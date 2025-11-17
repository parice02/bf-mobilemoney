import logging
import xml.etree.ElementTree as ET

from mobilemoney.base import BasePayment
from mobilemoney.utils import get_reference

# Configure logging
logger = logging.getLogger(__name__)


class GenericPayment(BasePayment):
    """
    Orange Money payment implementation.

    This class handles Orange Money API interactions including
    payment validation and XML request/response parsing.

    Attributes:
        url (str): The Orange Money API endpoint URL
    """

    def __init__(self, url="", phonenumber="", username="", password=""):
        """
        Initialize Orange Money payment instance.

        Args:
            url (str, optional): API endpoint URL. Defaults to "".
            phonenumber (str, optional): Merchant phone number. Defaults to "".
            username (str, optional): API username. Defaults to "".
            password (str, optional): API password. Defaults to "".

        Raises:
            ValueError: If url is not a string.
        """
        super().__init__(phonenumber, username, password)

        if not isinstance(url, str):
            raise ValueError("value 'url' must be type of 'str'")
        if not url.strip():
            logger.warning("Empty URL provided for Orange Money API")
        self._url = url

    @property
    def url(self):
        """Get the API endpoint URL."""
        return self._url

    @url.setter
    def url(self, value):
        """Set the API endpoint URL."""
        if not isinstance(value, str):
            raise ValueError("URL must be a string")
        self._url = value

    def parse_query(
        self,
        customer_phone: str,
        customer_otp: str,
        amount: int,
        libel: str,
        reference=None,
    ):
        """
        Parse payment request data into XML format for Orange Money API.

        Args:
            customer_phone (str): Customer's phone number
            customer_otp (str): Customer's OTP code
            amount (int): Payment amount
            libel (str): Payment description/label
            reference (str, optional): Transaction reference. Auto-generated if None.

        Returns:
            str: XML string formatted for Orange Money API

        Raises:
            ValueError: If any parameter has invalid type or value
        """
        # Validate inputs
        if not isinstance(customer_phone, str) or not customer_phone.strip():
            raise ValueError("Customer phone number must be a non-empty string")
        if not isinstance(customer_otp, str) or not customer_otp.strip():
            raise ValueError("Customer OTP must be a non-empty string")
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer")
        if not isinstance(libel, str) or not libel.strip():
            raise ValueError("Label must be a non-empty string")
        if reference is not None and not isinstance(reference, str):
            raise ValueError("Reference must be a string or None")

        logger.info(
            f"Creating payment request for phone: {customer_phone}, amount: {amount}"
        )

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
        ET.SubElement(root, "ext_txn_id").text = reference or get_reference()

        tree = ET.ElementTree(root)
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")

        return xml_string

    def parse_result(self, result: str):
        """
        Parse XML response from Orange Money API.

        Args:
            result (str): Raw XML response from API

        Returns:
            dict: Parsed response with status, message, and transaction ID
        """
        try:
            if not isinstance(result, str):
                raise ValueError("Result must be a string")

            root = ET.fromstring("<root>" + result + "</root>")

            status, message, trans_id = (
                root.find("status"),
                root.find("message"),
                root.find("transID"),
            )

            if (
                (status is not None)
                and (message is not None)
                and (trans_id is not None)
            ):
                response = {
                    "status": status.text,
                    "message": message.text,
                    "trans_id": trans_id.text,
                }
                logger.info(f"Successfully parsed API response: {response}")
                return response
            else:
                logger.error(f"Incomplete API response: {result}")
                return {
                    "message": "Erreur de retour de l'API OM - Réponse incomplète",
                    "status": "OM-500",
                    "trans_id": "Error",
                }
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
            return {
                "message": f"Erreur de parsing XML: {str(e)}",
                "status": "OM-501",
                "trans_id": "Error",
            }
        except Exception as e:
            logger.error(f"Unexpected error parsing result: {e}")
            return {
                "message": f"Erreur inattendue: {str(e)}",
                "status": "OM-502",
                "trans_id": "Error",
            }

    def validate_payment(
        self,
        customer_phone: str,
        customer_otp: str,
        amount: int,
        message: str,
        reference=None,
        verify_ssl=True,
    ):
        """
        Validate and process payment through Orange Money API.

        Args:
            customer_phone (str): Customer's phone number
            customer_otp (str): Customer's OTP code
            amount (int): Payment amount
            message (str): Payment description
            reference (str, optional): Transaction reference. Auto-generated if None.
            verify_ssl (bool, optional): Whether to verify SSL certificates. Defaults to True.

        Returns:
            dict: API response with status, message, and transaction ID

        Raises:
            requests.RequestException: If network request fails
            ValueError: If input validation fails
        """
        try:
            if not self._url:
                raise ValueError("API URL not configured")

            headers = {"content-type": "application/xml"}
            data = self.parse_query(
                customer_phone, customer_otp, amount, message, reference
            )

            response = self._make_request(
                method="POST",
                url=self._url,
                headers=headers,
                data=data,
                verify_ssl=verify_ssl,
            )

            response.raise_for_status()  # Raise an exception for bad status codes

            result = self.parse_result(response.text)
            self._logger.info(f"Parsed API response: {result}")
            return result

        except Exception as e:
            self._logger.error(f"Payment validation error: {e}")
            if "timeout" in str(e).lower():
                return {
                    "message": "Timeout de l'API Orange Money",
                    "status": "OM-503",
                    "trans_id": "Error",
                }
            elif "connection" in str(e).lower():
                return {
                    "message": "Erreur de connexion à l'API Orange Money",
                    "status": "OM-504",
                    "trans_id": "Error",
                }
            elif "http" in str(e).lower():
                return {
                    "message": f"Erreur HTTP: {e}",
                    "status": "OM-505",
                    "trans_id": "Error",
                }
            else:
                return {
                    "message": f"Erreur inattendue: {str(e)}",
                    "status": "OM-506",
                    "trans_id": "Error",
                }


class DevPayment(GenericPayment):
    """
    Development environment Orange Money payment implementation.

    This class is intended for use in development/testing environments.
    """

    def __init__(self, url, phonenumber="", username="", password=""):
        """
        Initialize development Orange Money payment instance.

        Args:
            url (str): Development API endpoint URL
            phonenumber (str, optional): Merchant phone number. Defaults to "".
            username (str, optional): Development API username. Defaults to "".
            password (str, optional): Development API password. Defaults to "".
        """
        super().__init__(url, phonenumber, username, password)
        logger.info("Initialized Orange Money DevPayment instance")


class Payment(GenericPayment):
    """
    Production environment Orange Money payment implementation.

    This class is intended for use in production environments.
    """

    def __init__(self, url, phonenumber="", username="", password=""):
        """
        Initialize production Orange Money payment instance.

        Args:
            url (str): Production API endpoint URL
            phonenumber (str, optional): Merchant phone number. Defaults to "".
            username (str, optional): Production API username. Defaults to "".
            password (str, optional): Production API password. Defaults to "".
        """
        super().__init__(url, phonenumber, username, password)
        logger.info("Initialized Orange Money Payment instance")
