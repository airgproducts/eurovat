import decimal
import unittest

from eurovat import VatRuleRegistry


class VatRateTest(unittest.TestCase):
    def setUp(self):
        self.registry = VatRuleRegistry()
    
    def assertRate(self, vat_rate, required_rate: str):
        first = vat_rate.rate
        second = decimal.Decimal(required_rate)

        self.assertEqual(first, second)
    
    def test_rate_de(self):
        self.assertRate(self.registry.get_vat_rate("DE"), "19")
    
    def test_rate_de_reduced_fruits(self):
        self.assertRate(self.registry.get_vat_rate("DE", "08050000"), "7")

    def test_rate_de_reduced_fresh_fruits(self):
        self.assertRate(self.registry.get_vat_rate("DE", "08059000"), "7")

    def test_rate_de_reduced_without_sacharrose(self):
        self.assertRate(self.registry.get_vat_rate("DE", "18061015"), "7")

if __name__ == "__main__":
    unittest.main()
