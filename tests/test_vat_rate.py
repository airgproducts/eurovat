import datetime
import decimal
import logging
import os
import unittest

from eurovat import VatRuleRegistry, get_vat_rate

logger = logging.getLogger(__name__)
dirname = os.path.dirname(os.path.abspath(__file__))


class VatRateTest(unittest.TestCase):
    registry: VatRuleRegistry

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.registry = VatRuleRegistry()
        cls.registry.date_begin = datetime.datetime(1990, 11, 21)
        cls.registry.fetch()

    def assertRate(self, vat_rate, required_rate: str):
        first = vat_rate.rate
        second = decimal.Decimal(required_rate)

        self.assertEqual(first, second)

    def test_rate_simple_at_saccharose(self):
        self.assertRate(get_vat_rate("AT", "18061015"), "10")

    def test_rate_de(self):
        self.assertRate(self.registry.get_vat_rate("DE"), "19")

    def test_rate_de_temporary_reduction(self):
        self.assertRate(
            self.registry.get_vat_rate(
                "DE", date=datetime.datetime(year=2020, month=10, day=5)
            ),
            "16",
        )

    def test_rate_ie_temporary_reduction(self):
        self.assertRate(
            self.registry.get_vat_rate(
                "IE", date=datetime.datetime(year=2020, month=10, day=5)
            ),
            "21",
        )
        self.assertRate(self.registry.get_vat_rate("IE"), "23")

    def test_rate_de_reduced_fruits(self):
        self.assertRate(self.registry.get_vat_rate("DE", "08050000"), "7")

    def test_rate_de_reduced_fresh_fruits(self):
        self.assertRate(self.registry.get_vat_rate("DE", "08059000"), "7")

    def test_rate_de_reduced_without_sacharrose(self):
        self.assertRate(self.registry.get_vat_rate("DE", "18061015"), "7")

    def test_rate_at_temporary_reduced_newspapers(self):
        self.assertRate(
            self.registry.get_vat_rate(
                "AT", "49020000", date=datetime.datetime(year=2016, month=10, day=5)
            ),
            "20",
        )

        # temporary reduction during covid
        self.assertRate(
            self.registry.get_vat_rate(
                "AT", "49020000", date=datetime.datetime(year=2019, month=10, day=5)
            ),
            "10",
        )


if __name__ == "__main__":
    unittest.main()
