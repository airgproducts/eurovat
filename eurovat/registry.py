import json
import os

from eurovat.states import states, EUState
from eurovat.rate import VatRules, VatRate
from eurovat.tedb import get_rates

class VatRuleRegistry:
    cache_dir = os.path.dirname(os.path.abspath(__file__))
    cache_filename = "data/vat_rules.json"

    custom_rules_filename = None

    vat_rules = {}

    def __init__(self, cachefile=None):
        filename = self._get_filename(cachefile)

        with open(filename) as infile:
            dct = json.load(infile)
        
        for key, _rules in dct.items():
            country = EUState.get(key)
            rules = [VatRate.fromdict(rule) for rule in _rules]
            self.vat_rules[key] = VatRules(country, rules)
    
    def _get_filename(self, filename=None, update_filename=False):
        if filename is None:
            filename = self.cache_filename
        elif update_filename:
            self.cache_filename = filename

        if not os.path.isabs(filename):
            filename = os.path.join(self.cache_dir, filename)
        else:
            if update_filename:
                self.cache_dir = None
        
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
    
    def store(self, filename=None) -> None:
        full_filename = self._get_filename(filename)

        with open(full_filename, "w") as outfile:
            json.dump({
                rule.country.iso_code: rule.as_list() for rule in self.vat_rules.values()
                }, outfile, indent=2)


if __name__ == "__main__":
    registry = VatRuleRegistry()
    registry.fetch()
    registry.store()
