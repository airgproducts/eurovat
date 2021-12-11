import json
import os
from typing import Dict, Optional
import datetime

from eurovat.states import states, EUState
from eurovat.rate import VatRules, VatRate
from eurovat.tedb import get_rates
from eurovat.data import vat_rules_file
from eurovat.cache import Cache, FilesystemCache
from eurovat.cache.filesystem import FilesystemCache

class VatRuleRegistry:
    cache: Cache = FilesystemCache(vat_rules_file)
    date_begin = None
    vat_rules: Dict[str, VatRules] = {}

    cache_last_update: float=0
    cache_auto_update: bool=True
    

    def __init__(self):
        self.load()
    
    def _get_filename(self):
        filename = self.cache_filename

        if not os.path.isabs(filename):
            filename = os.path.join(self.cache_dir, filename)
        
        return filename
    
    def get_vat_rate(self, to_country, cn_code=None, date: Optional[datetime.datetime]=None):
        if self.cache_auto_update:
            if self.cache_last_update < self.cache.get_mtime():
                self.load()

        if isinstance(to_country, EUState):
            to_country = to_country.iso_code

        return self.vat_rules[to_country.upper()].get_vat_rate(cn_code, date=date)

    def fetch(self, countries=None):
        if countries is None:
            countries = states
        
        self.vat_rules = {
            rule.country.iso_code: rule for rule in   
            get_rates(countries, self.date_begin)
        }

    def load(self):
        self.cache_last_update = self.cache.get_mtime()
        dct = self.cache.load()
        for key, _rules in dct.items():
            country = EUState.get(key)
            rules = [VatRate.fromdict(rule) for rule in _rules]
            self.vat_rules[key] = VatRules(country, rules)
    
    def store(self) -> None:
        self.cache.save({
            rule.country.iso_code: rule.as_list() for rule in self.vat_rules.values()
        })

    def update(self):
        self.fetch()
        self.store()


if __name__ == "__main__":
    registry = VatRuleRegistry()
    registry.update()
