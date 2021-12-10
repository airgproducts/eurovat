import os

dirname = os.path.dirname(os.path.abspath(__file__))

vat_rules_file = os.path.join(dirname, "vat_rules.json")

with open(os.path.join(dirname, "vies.xml")) as infile:
    vies_template = infile.read()
