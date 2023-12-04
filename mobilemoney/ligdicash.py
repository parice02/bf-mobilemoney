from typing import Any, List, Union, Dict
from pprint import pprint
import webbrowser

import requests  # TODO replace with urllib3


from .base import BasePayment

ligdicash_dev_url_with_redirect = (
    "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create"
)
ligdicash_prod_url_with_redirect = (
    "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create"
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

        response = requests.post(
            self._url,
            headers=headers,
            json={"commande": command},
            verify=verify_ssl,
        )
        pprint(response.request.headers)
        response = response.json()
        response = webbrowser.open(response["response_text"], new=2)

        return response

    def verify_token(self, token, verify_ssl=True):
        headers = {
            "content-type": "application/json",
            "Apikey": self._username,
            "authorization": f"Bearer {self._password}",
            "accept": "application/json",
        }
        response = requests.get(
            "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/confirm/",
            data={"invoiceToken": token},
            headers=headers,
            verify=verify_ssl,
        )

        if response["status"] == "completed":
            return True
        if response["status"] == "nocompleted":
            return False
        if response["status"] == "pending":
            return None

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
    def __init__(self, url=None, username="", password=""):
        url = ligdicash_prod_url_with_redirect if url is None else url
        super().__init__(url, username, password)
