from dataclasses import dataclass
from typing import Dict, List, Tuple

import pycountry


class EUState:
    iso_code: str
    name: str
    msa_id: int


    states_by_iso: Dict[str, "EUState"] = {}
    states_by_name: Dict[str, "EUState"] = {}

    def __init__(self, iso_code: str, name: str, msa_id: int):
        self.iso_code = iso_code.upper()
        self.name = name
        self.msa_id = msa_id
    
    @classmethod
    def register(cls, iso_code: str, name: str, msa_id: int) -> "EUState":
        instance = cls(iso_code, name, msa_id)
        cls.states_by_iso[instance.iso_code] = instance
        cls.states_by_name[instance.name.upper()] = instance

        return instance
    
    @classmethod
    def get(cls, query: str):
        if len(query) == 2:
            if query == "EL":
                query = "GR"
            if query == "UK":
                query = "GB"
            return cls.states_by_iso[query.upper()]
        else:
            return cls.states_by_name[query.upper()]
        
    @classmethod
    def all(cls):
        return cls.states_by_iso.values()


state_codes: List[Tuple[str, int]] = [
    ("AT", 1),
    ("BE", 2),
    ("BG", 3),
    ("CY", 4),
    ("CZ", 5),
    ("DE", 6),
    ("DK", 7),
    ("EE", 8),
    ("GR", 9),
    ("ES", 10),
    ("FI", 11),
    ("FR", 12),
    ("GB", 13),
    ("HR", 14),
    ("HU", 15),
    ("IE", 16),
    ("IT", 17),
    ("LT", 18),
    ("LU", 19),
    ("LV", 20),
    ("MT", 21),
    ("NL", 22),
    ("PL", 23),
    ("PT", 24),
    ("RO", 25),
    ("SE", 26),
    ("SI", 27),
    ("SK", 28)
]

states = []

for iso_code, msa_id in state_codes:
    name = pycountry.countries.lookup(iso_code).name
    states.append(EUState.register(iso_code, name, msa_id))
