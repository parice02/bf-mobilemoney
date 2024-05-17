import webbrowser

from mobilemoney import verify_ligdicash_payment_token, validate_ligdicash_payment


order = {
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
        "customer": "",
        "customer_firstname": "Nom du client",
        "customer_lastname": "Prénom du client",
        "customer_email": "tester@gligdicash.com",
        "external_id": "",
        "otp": "",
    },
    "store": {
        "name": "Nom de votre site ou de votre boutique",
        "website_url": "url de votre site ou de votre boutique",
    },
    "actions": {
        "cancel_url": "http://localhost",
        "return_url": "http://localhost",
        "callback_url": "http://localhost",
    },
    "custom_data": {
        "transaction_id": "2021000000001",
        "logfile": "202110210048426170b8ea884a9",
        "developpeur": "kaboretidiane",
    },
}

response = validate_ligdicash_payment(
    api_key="REV9DJR33TZ6J4I4O",
    api_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOjc3NCwiaWRfYWJvbm5lIjo4OTk0MiwiZGF0ZWNyZWF0aW9uX2FwcCI6IjIwMjQtMDQtMDggMDg6MzI6MjUifQ.4e1oGiEwhUZhaoIRfZRGYzg1kndXMNn59fXiq2yTpjI",
    command=order,
)

if "response_text" in response:
    webbrowser.open(response["response_text"])
