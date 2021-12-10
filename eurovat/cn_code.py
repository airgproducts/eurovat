from typing import List


class CnCode:
    code: str

    code_length = 8

    def __init__(self, code: str):
        if len(code) > self.code_length:
            raise ValueError(f"cn-code is too long ({len(code)}): {code}")
        
        self.code = code + "0" * (self.code_length-len(code))
    
    def __eq__(self, o: object):
        if isinstance(o, CnCode):
            return self.code == o.code
        elif isinstance(o, str):
            return self.code == o
        
        return False
    
    def __repr__(self):
        return f"<CnCode: {self.code}>"
    
    def _get_parent_code(self, remaining_length: int=2) -> "CnCode":
        return CnCode(self.code[:remaining_length] + "0" * (self.code_length-remaining_length))
    
    def get_hs_code(self) -> str:
        return self.code[:4]
    
    def get_parent_codes(self, min_chars: int=2) -> List["CnCode"]:
        _codes = [
            self._get_parent_code(6),
            self._get_parent_code(4),
            self._get_parent_code(2),
        ]

        codes = []

        for code in _codes:
            if code not in codes and code != self:
                codes.append(code)
        
        return codes

