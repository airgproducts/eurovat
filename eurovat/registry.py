import json
import os
from typing import Dict

from eurovat.states import states, EUState
from eurovat.rate import VatRules, VatRate
from eurovat.tedb import get_rates
from eurovat.data import vat_rules_file

class VatRuleRegistry:
    cache_filename = vat_rules_file
    cache_dir = ""

    custom_rules_filename = None

    vat_rules: Dict[str, VatRules] = {}

    def __init__(self):
        self.load()
    
    def _get_filename(self):
        filename = self.cache_filename

        if not os.path.isabs(filename):
            filename = os.path.join(self.cache_dir, filename)
        
        return filename
    
    def get_vat_rate(self, to_country, cn_code=None):
        if isinstance(to_country, EUState):
            to_country = to_country.iso_code

        return self.vat_rules[to_country.upper()].get_vat_rate(cn_code)

    def fetch(self, countries=None):
        if countries is None:
            countries = states
        
        self.vat_rules = {
            rule.country.iso_code: rule for rule in   
            get_rates(countries)
        }

    def load(self):
        dct = self.load_data()
        for key, _rules in dct.items():
            country = EUState.get(key)
            rules = [VatRate.fromdict(rule) for rule in _rules]
            self.vat_rules[key] = VatRules(country, rules)
    
    def load_data(self) -> Dict[str, object]:
        filename = self._get_filename()

        with open(filename) as infile:
            return json.load(infile)
    
    def store(self) -> None:
        full_filename = self._get_filename()

        with open(full_filename, "w") as outfile:
            json.dump({
                rule.country.iso_code: rule.as_list() for rule in self.vat_rules.values()
                }, outfile, indent=2)

    def update(self):
        self.fetch()
        self.store()


if __name__ == "__main__":
    registry = VatRuleRegistry()
    registry.update()
