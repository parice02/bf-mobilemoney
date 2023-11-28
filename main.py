from datetime import datetime
from random import randint
import webbrowser

from mobilemoney import validate_ligdicash_payment

today = datetime.now()

trans_id = f"LDG{(today.year)}{today.month}{today.day}{today.hour}{today.minute}{today.second}{today.microsecond}C{randint(5, 100000)}"

command = {
    "invoice": {
        "items": [
            {
                "name": "Nom du produit ou Service",
                "description": " Description du produit ou Service ",
                "quantity": 1,
                "unit_price": 100,
                "total_price": 100,
            }
        ],
        "total_amount": 100,
        "devise": "XOF",
        "description": " Description du contenu de la facture(Achat de jus de fruits)",
        "customer": "+22664712648",
        "customer_firstname": "Nom du client",
        "customer_lastname": "Prénom du client",
        "customer_email": "tester@gligdicash.com",
        # "external_id": "",
        # "otp": "",
    },
    "store": {
        "name": "Nom de votre site ou de votre boutique",
        "website_url": "https://etimbre.dgi.bf",
    },
    "actions": {
        "cancel_url": "http://localhost",
        "return_url": "http://localhost",
        "callback_url": "http://localhost",
    },
    "custom_data": {
        "transaction_id": trans_id,  # id à générer
        # "logfile": "202110210048426170b8ea884a9",
        # "developpeur": "kaboretidiane",
    },
}


response = validate_ligdicash_payment(
    api_key="TKC8O8BX9TAA8EL0G",  # SUGSFAKICRVXD1OSH
    api_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOiIxMjgyMSIsImlkX2Fib25uZSI6MzUzNDYyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyMy0xMS0yOCAwOToyMzo0MiJ9.zr8Vs1vZgkPSJIfjhvDfnEtGv2qZrvQvx4BKFGJKxP8",
    command=command,
)
print(response)
response = webbrowser.open_new_tab(response["response_text"])

print(response)

"""
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOiIxMjQ5NiIsImlkX2Fib25uZSI6MzUzNDYyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyMy0xMS0xMCAxNDo1NTo0NCJ9.vlSBW5zvwMAAaupXZrZi5GRrf79Ctuka6Rz1Uprbf54
"""
