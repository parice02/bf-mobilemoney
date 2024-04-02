# Mobile Money Payment API (Burkina Faso)

API non officiel pour les paiements mobiles Orange Money, Moov Money et Ligdicash au Burkina Faso


## Avant l'installation

1. Obtenir un compte API avec Orange/Moov/Ligdicash (username, password, phonenumber, certificats, ....)
2. Installer les certificats fournis par l'opérateur s'il y'en


## Dépendances

- python = "^3.9"
- requests = "^2.31.0"

## Installation

```bash
pip install https://github.com/parice02/bf-mobilemoney.git
```


## Cas d'utilisation

```python
from mobilemoney import validate_om_prod_payment

# exemple de paiement avec orange money

username = "<Your OM API username>"
password = "<Your OM API password>"
phonenumber = "<Your OM API phone number>"
customer_phone = "<Your customer phone number>"
customer_otp = "<Your customer OTP code>"
amount = "<the amount>"
message = "<a message for user>"


response = validate_om_prod_payment(
    username, password, phonenumber, customer_phone, customer_otp, amount, message
)
print(response)
```

## Contribution

Les contributions sont libres.
