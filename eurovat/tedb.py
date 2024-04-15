from typing import Union, Optional, List, Dict
import requests
import datetime
import time
import decimal

from eurovat.states import EUState
from eurovat.rate import VatRate, VatRules

query_url = "https://ec.europa.eu/taxation_customs/tedb/rest-api/vatSearch"
dateformat = "%Y/%m/%d"


def get_rates(
    countries: List[Union[str, EUState]],
    date_from: Optional[datetime.date] = None,
    date_to: Optional[datetime.date] = None,
) -> List[VatRules]:
    countries_lst = []

    for country in countries:
        if isinstance(country, EUState):
            countries_lst.append(country.msa_id)
        else:
            countries_lst.append(EUState.get(country).msa_id)

    if date_to is None:
        date_to = datetime.date.today()

    if date_from is None:
        date_from_str = None
    else:
        date_from_str = date_from.strftime(dateformat)

    request = requests.post(
        url=query_url,
        json={
            "searchForm": {
                "selectedMemberStates": countries_lst,
                "dateFrom": date_from_str,
                "dateTo": date_to.strftime(dateformat),
            }
        },
    )

    assert request.status_code == 200

    data = request.json()

    rates: Dict[str, List[VatRate]] = {}

    for row in data["result"]:
        assert row["type"] in ("STANDARD", "REDUCED")
        country_code = row["isoCode"]
        reduced = row["type"] != "STANDARD"
        for rate in row["rates"]:
            rate_value = decimal.Decimal(rate["value"])

            cn_codes = []
            if rate["cnCodes"]:
                cn_codes = [code["code"] for code in rate["cnCodes"]]

            cpa_codes = []
            if rate["cpaCodes"]:
                cpa_codes = [
                    code.get("code", None) for code in rate["cpaCodes"]
                ]

            start_date = time.mktime(
                datetime.datetime.strptime(rate["situationOn"], "%Y/%m/%d").timetuple()
            )

            rates.setdefault(country_code, [])
            rates[country_code].append(
                VatRate(
                    reduced=reduced,
                    rate=rate_value,
                    situation_on=start_date,
                    cn_codes=cn_codes,
                    cpa_codes=cpa_codes,
                    category=rate["category"],
                    description=rate["comments"] or "",
                )
            )

    # WORKAROUND for missing rule:
    rates["DE"].append(
        VatRate(
            reduced=False,
            rate=decimal.Decimal("16"),
            cn_codes=[],
            cpa_codes=[],
            situation_on=datetime.datetime(2020, 7, 1).timestamp(),
        )
    )

    # canary-islands-reduced rate
    spanish_standard_rates = filter(lambda el: not el.reduced, rates["ES"])
    for rate_es in spanish_standard_rates:
        if rate_es.description:
            rate_es.reduced = True

    return [
        VatRules(EUState.get(country_name), rate_lst)
        for country_name, rate_lst in rates.items()
    ]
