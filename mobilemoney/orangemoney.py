from typing import Any, List, Union, Dict

import xml.etree.ElementTree as ET
import requests  # TODO replace with urllib3

from .base import BasePayment

orange_dev_url = "https://testom.orange.bf:9008/payment"
orange_prod_url = "https://apiom.orange.bf:9007/payment"

class GenericPayment(BasePayment):
    def __init__(self, url="", phonenumber="", username="", password=""):
        super().__init__(phonenumber, username, password)

        if not isinstance(url, str):
            raise ValueError("value 'url' must be type of 'str'")
        self._url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @url.deleter
    def url(self):
        del self._url

    def parse_query(
        self, customer_phone: str, customer_otp: str, amount: int, libel: str
    ):
        root = ET.Element("COMMAND")

        # Ajouter les éléments enfants à l'élément racine
        ET.SubElement(root, "TYPE").text = "OMPREQ"
        ET.SubElement(root, "customer_msisdn").text = f"{customer_phone}"
        ET.SubElement(root, "merchant_msisdn").text = self._phonenumber
        ET.SubElement(root, "api_username").text = self._username
        ET.SubElement(root, "api_password").text = self._password
        ET.SubElement(root, "amount").text = f"{amount}"
        ET.SubElement(root, "PROVIDER").text = "101"
        ET.SubElement(root, "PROVIDER2").text = "101"
        ET.SubElement(root, "PAYID").text = "12"
        ET.SubElement(root, "PAYID2").text = "12"
        ET.SubElement(root, "otp").text = f"{customer_otp}"
        ET.SubElement(root, "reference_number").text = libel
        ET.SubElement(root, "ext_txn_id").text = ""

        tree = ET.ElementTree(root)
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")

        return xml_string

    def parse_result(result: str):
        import re

        # root = ET.Element("result")
        # child = ET.fromstring(result)
        # root.append(child)

        # status, message = root.find("status"), root.find("message")

        # if (status is not None) and (message is not None):
        #     return {"status": status.text, "message": message.text}
        # else:
        #     return {
        #         "message": "Erreur de retour de l'API OM",
        #         "status": "500",
        #     }

        pattern = r"<status>(?P<status>.*)</status>.*?<message>(?P<message>.*)</message>.*?<transID>(?P<transID>.*)</transID>"
        matches = re.search(pattern, result)
        if matches:
            return {
                "status": matches["status"],
                "message": matches["message"],
                "trans_id": matches["transID"],
            }
        return {
            "message": "Erreur de retour de l'API OM",
            "status": "500",
            "trans_id": None,
        }

    def validate_payment(
        self,
        customer_phone: str,
        customer_otp: str,
        amount: int,
        message: str,
        verify_ssl=True,
    ):
        headers = {"content-type": "application/xml"}
        data = self.parse_query(customer_phone, customer_otp, amount, message)
        response = requests.post(
            self._url, headers=headers, data=data, verify=verify_ssl
        )
        return self.parse_result(response.text)


class DevPayment(GenericPayment):
    def __init__(self, phonenumber="", username="", password=""):
        url = orange_dev_url
        super().__init__(url, phonenumber, username, password)


class Payment(GenericPayment):
    def __init__(self, phonenumber="", username="", password=""):
        url = orange_prod_url
        super().__init__(url, phonenumber, username, password)
