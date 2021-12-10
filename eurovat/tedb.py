from typing import Union, Optional, List, Dict
import requests
import datetime
import decimal
import json

from eurovat.states import EUState, states
from eurovat.rate import VatRate, VatRules

query_url = "https://ec.europa.eu/taxation_customs/tedb/vatSearchResult.json"
dateformat = "%Y/%m/%d"

def get_rates(countries: List[Union[str, EUState]], date_from: Optional[datetime.date]=None, date_to: Optional[datetime.date]=None) -> List[VatRules]:
    countries_lst = []

    for country in countries:
        if isinstance(country, EUState):
            countries_lst.append(country.msa_id)
        else:
            countries_lst.append(EUState.get(country).msa_id)

    if date_to is None:
        date_to = datetime.date.today()

    if date_from is None:
        date_from_str = ""
    else:
        date_from_str = date_from.strftime(dateformat)

    request = requests.post(
        url=query_url,
        params={
        "selectedMemberStates": countries_lst,
        "dateFrom": date_from_str.encode(),
        "dateTo": date_to.strftime(dateformat).encode()
        })
    
    data = request.json()

    rates = {}
    
    for row in data:
        assert row["type"] in ("STANDARD", "REDUCED")
        country_code = row["memberState"]["defaultCountryCode"]
        reduced = row["type"] != "STANDARD"
        rate = decimal.Decimal(row["rate"]["value"])

        cn_codes = [
            code["key"]["code"]
            for code in row["cnCodes"]
        ]

        cpa_codes = [
            code["key"]["code"]
            for code in row["cpaCodes"]

        ]

        rates.setdefault(country_code, [])
        rates[country_code].append(
            VatRate(
                reduced=reduced,
                rate = rate,
                cn_codes = cn_codes,
                cpa_codes = cpa_codes,
                category = row["category"],
                description = row["comments"] or ""
            )
        )
    
    return [
        VatRules(EUState.get(country_name), rate_lst)
        
        for country_name, rate_lst in rates.items()
    ]


    
if __name__ == "__main__":
    rates = get_rates(["DE"])
    with open("./rates.json", "w") as outfile:
        json.dump(rates["DE"].as_list(), outfile, indent=4)
