import decimal
import unittest

from eurovat import VatNumber


class VatNumberTest(unittest.TestCase):    
    def test_vatnr_airgproducts(self):
        vat_nr = VatNumber("ATU71738505")
        result = vat_nr.check_vies()
        self.assertTrue(result.valid)
        self.assertEqual(result.country_code, "AT")
        self.assertEqual(result.name, "AirG distribution GmbH")
        self.assertEqual(result.number, "U71738505")
        self.assertEqual(result.address, "Bachlechnerstraße 21\nAT-6020 Innsbruck")
    
    def test_invalid_vatnr(self):
        vat_nr = VatNumber("ATU71738504")
        result = vat_nr.check_vies()

        self.assertFalse(result.valid)
    
    def test_ratelimit(self):
        vat_nr = VatNumber("ATU71738505")
        for i in range(10):
            result = vat_nr.check_vies()

        

if __name__ == "__main__":
    unittest.main()
