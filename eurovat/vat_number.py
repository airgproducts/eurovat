import datetime
import logging
import re
import time
from typing import Optional

import requests
from xml.etree import ElementTree
from eurovat.data import vies_template


logger = logging.getLogger(__name__)
vies_url = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
vies_url = "https://ec.europa.eu/taxation_customs/vies/services/checkVatService"


class ViesResult:
    result_string: str
    
    number: str=""
    country_code: str=""

    request_date: Optional[datetime.date]=None
    valid: bool=False

    name: str=""
    address: str=""

    _NS_SOAP = "{http://schemas.xmlsoap.org/soap/envelope/}"
    _NS_VIES = "{urn:ec.europa.eu:taxud:vies:services:checkVat:types}"

    def __init__(self, result: str):
        self.result_string = result
        self.parse()
    
    def __repr__(self):
        return f"ViesResult: {self.valid} ({self.request_date})"
    
    def parse(self):

        tree = ElementTree.fromstring(self.result_string)

        response = tree.find('./' + self._NS_SOAP + 'Body/' + self._NS_VIES + 'checkVatResponse')

        self.number = response.find('./' + self._NS_VIES + 'vatNumber').text
        self.country_code = response.find('./' + self._NS_VIES + 'countryCode').text

        date_str = response.find('./' + self._NS_VIES + 'requestDate').text
        if date_str:
            self.request_date = datetime.datetime.strptime(date_str, "%Y-%m-%d%z").date()
        
        valid = response.find('./' + self._NS_VIES + 'valid').text
        if valid == "true":
            self.valid = True

        self.name = response.find('./' + self._NS_VIES + 'name').text
        self.address = response.find('./' + self._NS_VIES + 'address').text


class VatNumber:
    code: str

    def __init__(self, vat: str):
        self.code = self.normalize(vat)

    @property
    def country_code(self):
        return self.code[:2]
    
    @property
    def vat_code(self):
        return self.code[2:]

    @staticmethod
    def normalize(vat: str) -> str:
        new_vat = "".join(re.findall(r"[0-9A-Z]", vat.upper()))

        if not re.match(r"([A-Z]{2})(U?[0-9]{8,9})", new_vat):
            raise ValueError(f"invalid vat: {new_vat}")

        return new_vat

    def check_vies(self) -> ViesResult:
        payload = vies_template.format(
            country_code = self.country_code,
            vat_code = self.vat_code
        )        

        num_requests = 0

        while num_requests < 5:
            result = requests.post(
                vies_url,
                data=payload,
                headers={
                    'Content-Type': 'text/xml; charset=utf-8'
                    }
            )

            if result.status_code == 200:
                return ViesResult(result.text)
            
            logger.warning(f"unresolved vies check, trying again")
            time.sleep(1)
        
        raise Exception(f"could not check vies")


if __name__ == "__main__":
    vat = VatNumber("ATU71738505")
    vat.check_vies()
