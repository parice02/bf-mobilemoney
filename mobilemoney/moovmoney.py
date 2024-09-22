import requests  # TODO replace with urllib3
from requests.auth import HTTPBasicAuth

from mobilemoney.base import BasePayment
from mobilemoney.utils import get_reference


SEND_OTP_OPTIONS = [
    "process-create-mror-otp",
    "process-mror-resend-otp",
]


class GenericPayment(BasePayment):
    def __init__(self, url="", username="", password=""):
        super().__init__(None, username, password)

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
        self,
        customer_phone: str,
        customer_otp: str,
        amount: int,
        message: str,
        otp_trans_id: str,
        reference: str = None,
    ):
        return {
            "request-id": reference or get_reference(),
            "destination": f"226{customer_phone}",
            "amount": f"{amount}",
            "remarks": f"{message}",
            "extended-data": {
                "module": "MERCHOTPPAY",
                "otp": f"{customer_otp}",
                "ext1": "Vous avez payé pour 1",
                "ext2": "Vous avez payé pour 2",
                "trans-id": f"{otp_trans_id}",
            },
        }

    def _send_otp(
        self,
        customer_phone: str,
        amount: int,
        verify_ssl=False,
        option="",
        reference: str = None,
    ):
        if option not in SEND_OTP_OPTIONS:
            raise ValueError(
                f"'option' parameter must be one of '{','.join(SEND_OTP_OPTIONS)}'"
            )
        data = {
            "request-id": reference or get_reference(),
            "destination": f"226{customer_phone}",
            "amount": amount,
            "remarks": "Merchant Payment with OTP",
            "extended-data": {"module": "MERCHOTPPAY"},
        }

        headers = {
            "content-type": "application/json",
            "command-id": option,
        }

        response = requests.post(
            self._url,
            headers=headers,
            json=data,
            auth=HTTPBasicAuth(self._username, self._password),
            verify=verify_ssl,
        )

        print("MM API (re)send OTP request header", response.request.headers)
        print("MM API (re)send OTP request body", response.request.body.decode())
        print("MM API (re)send OTP response status", response.status_code)
        print("MM API (re)send OTP response content", response.text)

        return response.json()

    def send_otp(
        self,
        customer_phone: str,
        amount: int,
        verify_ssl=False,
        reference: str = None,
    ):
        return self._send_otp(
            customer_phone, amount, verify_ssl, SEND_OTP_OPTIONS[0], reference
        )

    def resend_otp(
        self,
        customer_phone: str,
        amount: int,
        verify_ssl=False,
        reference: str = None,
    ):
        return self._send_otp(
            customer_phone, amount, verify_ssl, SEND_OTP_OPTIONS[1], reference
        )

    def validate_payment(
        self,
        customer_phone: str,
        customer_otp: str,
        amount: int,
        message: str,
        otp_trans_id: str,
        verify_ssl=False,
        reference: str = None,
    ):
        headers = {
            "content-type": "application/json",
            "command-id": "process-commit-otppay",
        }

        response = requests.post(
            self._url,
            headers=headers,
            json=self.parse_query(
                customer_phone,
                customer_otp,
                amount,
                message,
                otp_trans_id,
                reference,
            ),
            auth=HTTPBasicAuth(self._username, self._password),
            verify=verify_ssl,
        )
        print("MM API payment request header", response.request.headers)
        print("MM API payment request body", response.request.body)
        print("MM API payment response status", response.status_code)
        print("MM API payment response content", response.text)
        return response.json()


class DevPayment(GenericPayment):
    def __init__(self, url, username="", password=""):
        super().__init__(url, username, password)


class Payment(GenericPayment):
    def __init__(self, url, username="", password=""):
        super().__init__(url, username, password)
