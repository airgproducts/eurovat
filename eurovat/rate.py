from typing import List, Dict, Optional
import enum
import decimal
import dataclasses
import datetime

from eurovat.states import EUState
from eurovat.cn_code import CnCode


@dataclasses.dataclass
class VatRate:
    reduced: bool
    rate: decimal.Decimal

    cn_codes: List[str]
    cpa_codes: List[str]

    category: str=""
    description: str=""
    situation_on: Optional[float]=None

    def __post_init__(self):
        for i, code in enumerate(self.cn_codes):
            if len(code) != 8:
                code = code.replace(" ", "")
                code += "0" * (8-len(code))

                self.cn_codes[i] = code
    
    @property
    def start_date(self):
        if self.situation_on is not None:
            return datetime.datetime.fromtimestamp(self.situation_on)
    
    @property
    def rate_multiplier(self):
        return self.rate / 100
    
    def asdict(self):
        dct = dataclasses.asdict(self)
        dct["rate"] = str(self.rate)

        return dct
    
    @classmethod
    def fromdict(cls, dct):
        data = dct.copy()
        data["rate"] = decimal.Decimal(data["rate"])

        return cls(**data)




@dataclasses.dataclass
class VatRules:
    country: EUState
    vat_rates: List[VatRate]

    _vat_rates_standard: List[VatRate] = dataclasses.field(default_factory=lambda: [])
    _vat_rates_reduced_cn: Dict[str, List[VatRate]] = dataclasses.field(default_factory=lambda: {})
    _vat_rates_reduced_cpa: Dict[str, List[VatRate]] = dataclasses.field(default_factory=lambda: {})

    def __post_init__(self):
        self._index()

    def _index(self):
        self._vat_rates_standard = []
        self._vat_rates_reduced_cn = {}
        self._vat_rates_reduced_cpa = {}

        for vat_rate in self.vat_rates:
            if vat_rate.reduced:
                for code in vat_rate.cn_codes:
                    self._vat_rates_reduced_cn.setdefault(code, [])
                    self._vat_rates_reduced_cn[code].append(vat_rate)

                for code in vat_rate.cpa_codes:
                    self._vat_rates_reduced_cpa.setdefault(code, [])
                    self._vat_rates_reduced_cpa[code].append(vat_rate)
            
            else:
                self._vat_rates_standard.append(vat_rate)
        
        for lst in self._vat_rates_reduced_cn.values():
            lst.sort(key=lambda el: -el.situation_on)

        for lst in self._vat_rates_reduced_cpa.values():
            lst.sort(key=lambda el: -el.situation_on)
        
        self._vat_rates_standard.sort(key=lambda el: -el.situation_on)


    def get_vat_rate(self, cn_code=None, cpa_code=None, date: Optional[datetime.datetime]=None) -> VatRate:
        rates: List[VatRate] = []

        if cn_code is not None:
            if isinstance(cn_code, str):
                cn_code = CnCode(cn_code)

            cn_codes = [cn_code] + cn_code.get_parent_codes()

            for _cn_code in cn_codes:
                try:
                    rates += self._vat_rates_reduced_cn[_cn_code.code]
                except KeyError:
                    pass

        if cpa_code is not None:
            try:
                rates += self._vat_rates_reduced_cpa[cpa_code]
            except KeyError:
                pass
        
        rates += self._vat_rates_standard

        # filter by date
        if date:
            timestamp = date.timestamp()

            for rate in rates:
                if rate.situation_on is not None and rate.situation_on <= timestamp:
                    return rate
            
            return self._vat_rates_standard[0]
        
        return rates[0]
    
    def as_list(self):
        return [
            obj.asdict() for obj in self.vat_rates
        ]
