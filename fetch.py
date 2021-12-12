import os

import eurovat
from eurovat.states import states

dirname = os.path.dirname(os.path.abspath(__file__))

registry = eurovat.VatRuleRegistry()
registry.update()

with open(os.path.join(dirname, "Rates.md"), "w") as outfile:
    outfile.write("# Standard rates in the EU\n\n")
    for country in states:
        rate = registry.get_vat_rate(country)
        outfile.write(f"- {country.iso_code}: {rate.rate}\n")
