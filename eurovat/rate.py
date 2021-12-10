from typing import List, Dict
import enum
import decimal
import dataclasses

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

    def __post_init__(self):
        for i, code in enumerate(self.cn_codes):
            if len(code) != 8:
                code = code.replace(" ", "")
                code += "0" * (8-len(code))

                self.cn_codes[i] = code
    
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
    _vat_rates_reduced_cn: Dict[str, VatRate] = dataclasses.field(default_factory=lambda: {})
    _vat_rates_reduced_cpa: Dict[str, VatRate] = dataclasses.field(default_factory=lambda: {})

    def __post_init__(self):
        self._index()

    def _index(self):
        self._vat_rates_standard = []
        self._vat_rates_reduced_cn = {}
        self._vat_rates_reduced_cpa = {}

        for vat_rate in self.vat_rates:
            if vat_rate.reduced:
                for code in vat_rate.cn_codes:
                    self._vat_rates_reduced_cn[code] = vat_rate

                for code in vat_rate.cpa_codes:
                    self._vat_rates_reduced_cpa[code] = vat_rate
            
            else:
                self._vat_rates_standard.append(vat_rate)       


    def get_vat_rate(self, cn_code=None, cpa_code=None) -> VatRate:
        if cn_code is not None:
            if isinstance(cn_code, str):
                cn_code = CnCode(cn_code)

            cn_codes = [cn_code] + cn_code.get_parent_codes()

            for cn_code in cn_codes:
                if cn_code.code in self._vat_rates_reduced_cn:
                    return self._vat_rates_reduced_cn[cn_code.code]
        
        if cpa_code is not None:
            if cpa_code in self._vat_rates_reduced_cpa:
                return self._vat_rates_reduced_cpa[cpa_code]
            
        return self._vat_rates_standard[0]
    
    def as_list(self):
        return [
            obj.asdict() for obj in self.vat_rates
        ]
