from requests.auth import HTTPBasicAuth

from mobilemoney.base import BasePayment

onatel_dev_url = "https://196.28.245.227/tlcfzc_gw/api/gateway/3pp/transaction/process"
onatel_prod_url = (
    "https://196.28.245.227/tlcfzc_gw_prod/mbs-gateway/gateway/3pp/transaction/process"
)

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
        libel: str,
        otp_trans_id: str,
    ):
        return {
            "request-id": "",
            "destination": f"226{customer_phone}",
            "amount": f"{amount}",
            "remarks": f"{libel}",
            "extended-data": {
                "module": "MERCHOTPPAY",
                "otp": f"{customer_otp}",
                "ext1": "Vous avez payé pour 1",
                "ext2": "Vous avez payé pour 2",
                "trans-id": f"{otp_trans_id}",
            },
        }

    def _send_otp(self, customer_phone: str, amount: int, verify_ssl=False, option=""):
        if option not in SEND_OTP_OPTIONS:
            raise ValueError(
                f"'option' parameter must be one of '{','.join(SEND_OTP_OPTIONS)}'"
            )
        data = {
            "request-id": "",
            "destination": f"226{customer_phone}",
            "amount": amount,
            "remarks": "Merchant Payment with OTP",
            "extended-data": {"module": "MERCHOTPPAY"},
        }

        headers = {
            "content-type": "application/json",
            "command-id": option,
        }

        response = self.post(
            self._url,
            headers=headers,
            json=data,
            auth=HTTPBasicAuth(self._username, self._password),
            verify=verify_ssl,
        )

        return response.json()

    def send_otp(self, customer_phone: str, amount: int, verify_ssl=False):
        return self._send_otp(customer_phone, amount, verify_ssl, SEND_OTP_OPTIONS[0])

    def resend_otp(self, customer_phone: str, amount: int, verify_ssl=False):
        return self._send_otp(customer_phone, amount, verify_ssl, SEND_OTP_OPTIONS[1])

    def validate_payment(
        self,
        customer_phone: str,
        customer_otp: str,
        amount: int,
        message: str,
        otp_trans_id,
        verify_ssl=False,
    ):
        headers = {
            "content-type": "application/json",
            "command-id": "process-commit-otppay",
        }

        response = self.post(
            self._url,
            headers=headers,
            json=self.parse_query(
                customer_phone, customer_otp, amount, message, otp_trans_id
            ),
            auth=HTTPBasicAuth(self._username, self._password),
            verify=verify_ssl,
        )
        return response.json()


class DevPayment(GenericPayment):
    def __init__(self, phonenumber="", username="", password=""):
        url = onatel_dev_url
        super().__init__(url, phonenumber, username, password)


class Payment(GenericPayment):
    def __init__(self, phonenumber="", username="", password=""):
        url = onatel_prod_url
        super().__init__(url, phonenumber, username, password)
