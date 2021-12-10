import decimal
import unittest
from typing import List

from eurovat import CnCode


class CnCodeTest(unittest.TestCase):    
    def assertCode(self, code: CnCode, target_code: str):
        self.assertEqual(code.code, target_code)
    
    def assertParents(self, code: CnCode, parent_codes: List[str]):
        for code, target_code in zip(code.get_parent_codes(), parent_codes):
            self.assertCode(code, target_code)
    
    def test_cn_code_init(self):
        code = CnCode("0805")
        self.assertCode(code, "08050000")

    def test_cn_code_parent(self):
        code = CnCode("18061015")
        self.assertParents(code, [
            "18061000",
            "18060000",
            "18000000"
        ])

if __name__ == "__main__":
    unittest.main()
