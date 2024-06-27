import xml.etree.ElementTree as ET
import requests  # TODO replace with urllib3

from mobilemoney.base import BasePayment
from mobilemoney.utils import get_reference


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
        ET.SubElement(root, "ext_txn_id").text = get_reference()

        tree = ET.ElementTree(root)
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")

        return xml_string

    def parse_result(self, result: str):
        root = ET.fromstring("<root>" + result + "</root>")

        status, message, trans_id = (
            root.find("status"),
            root.find("message"),
            root.find("transID"),
        )

        if (status is not None) and (message is not None) and (trans_id is not None):
            return {
                "status": status.text,
                "message": message.text,
                "trans_id": trans_id.text,
            }
        else:
            return {
                "message": "Erreur de retour de l'API OM",
                "status": "OM-500",
                "trans_id": "Error",
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

        print("OM API payment request header", response.request.headers)
        print("OM API payment request body", response.request.body.decode())
        print("OM API payment response status", response.status_code)
        print("OM API payment response content", response.text)
        result = self.parse_result(response.text)
        print("OM API payment response content parsed ", result)
        return result


class DevPayment(GenericPayment):
    def __init__(self, url, phonenumber="", username="", password=""):
        super().__init__(url, phonenumber, username, password)


class Payment(GenericPayment):
    def __init__(self, url, phonenumber="", username="", password=""):
        super().__init__(url, phonenumber, username, password)
