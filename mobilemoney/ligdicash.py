import json

from mobilemoney.base import BasePayment

ligdicash_dev_url_with_redirect = (
    "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create/"
)
ligdicash_prod_url_with_redirect = (
    "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create/"
)
verify_url_with_redirect = (
    "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/confirm/"
)


class GenericPaymentWithRedirect(BasePayment):
    def __init__(self, url="", username="", password=""):
        super().__init__(None, username, password)

        if not isinstance(url, str):
            raise ValueError("value 'url' must be type of 'str'")
        self._url = url

    def validate_payment(self, command={}, verify_ssl=True):
        """
        Validate a payment
            - command param must be :
                {
                    "invoice": {
                        "items": [
                        {
                            "name": "Nom du produit ou Service",
                            "description": " Description du produit ou Service ",
                            "quantity": 1,
                            "unit_price": 100,
                            "total_price": 100
                         }
                      ],
                        "total_amount": 100,
                        "devise": "XOF",
                        "description": " Description du contenu de la facture(Achat de jus de fruits)",
                        "customer": "",
                        "customer_firstname": "Nom du client",
                        "customer_lastname": "Prénom du client",
                        "customer_email": "tester@gligdicash.com",
                        "external_id": "",
                        "otp": ""
                    },
                    "store": {
                        "name": "Nom de votre site ou de votre boutique",
                        "website_url": "url de votre site ou de votre boutique"
                    },
                    "actions": {
                        "cancel_url": "http://localhost",
                        "return_url": "http://localhost",
                        "callback_url": "http://localhost"
                    },
                   "custom_data": {
                        "transaction_id": "2021000000001",
                        "logfile": "202110210048426170b8ea884a9",
                        "developpeur": "kaboretidiane"
                    }
                }

            - response will be:
                {
                    "response_code": "00",
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9pbnZvaWNlIjoiMTU0NTkwMTIiLCJzdGFydF9kYXRlIjoiMjAyMy0wMi0yMyAxODoyNDoxMiIsImV4cGlyeV9kYXRlIjoxNjc3MjU5NDUyfQ.U9GwpBQpZwW1YdWD_0Zla9-Uy-sUV7zDn4Nobtfc33M",
                    "response_text": "https://client.ligdicash.com/directpayment/invoice/   eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9pbnZvaWNlIjoiMTU0NTkwMTIiLCJzdGFydF9kYXRlIjoiMjAyMy0wMi0yMyAxODoyNDoxMiIsImV4cGlyeV9kYXRlIjoxNjc3MjU5NDUyfQ.U9GwpBQpZwW1YdWD_0Zla9-Uy-sUV7zDn4Nobtfc33M",
                    "description": "",
                    "custom_data": {
                        "transaction_id": "2021000000001",
                        "logfile": "2023022318241263f7af4ccc792",
                        "developpeur": "kaboretidiane",
                    },
                    "wiki": "https://client.ligdicash.com/wiki/createInvoice",
                }
        """
        headers = {
            "Content-Type": "application/json",
            "Apikey": self._username,
            "Authorization": f"Bearer {self._password}",
            "Accept": "application/json",
        }

        return self.post(
            self._url,
            headers=headers,
            json={"commande": command},
            verify=verify_ssl,
        )

    def verify_token(self, token, verify_ssl=True):
        headers = {
            "content-type": "application/json",
            "Apikey": self._username,
            "authorization": f"Bearer {self._password}",
            "accept": "application/json",
        }
        response = self.get(
            verify_url_with_redirect,
            params={"invoiceToken": token},
            headers=headers,
            verify=verify_ssl,
        )
        response_json = response.json()

        if response_json.get("status", "") == "completed":
            return True, response
        elif response_json.get("status", "") == "nocompleted":
            return False, response
        elif response_json.get("status", "") == "pending":
            return None, response
        return None, response

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @url.deleter
    def url(self):
        del self._url


class Payment(GenericPaymentWithRedirect):
    def __init__(self, username="", password=""):
        url = ligdicash_prod_url_with_redirect
        super().__init__(url, username, password)
