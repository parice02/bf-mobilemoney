from mobilemoney.base import BasePayment
from mobilemoney.orangemoney import (
    GenericPayment as OMGenericPayement,
    Payment as OMPayment,
    DevPayment as OMDevPayment,
)

from mobilemoney.moovmoney import (
    GenericPayment as MMGenericPayement,
    Payment as MMPayment,
    DevPayment as MMDevPayment,
)


def validate_om_prod_payment(
    username: str,
    password: str,
    phonenumber: str,
    customer_phone: str,
    customer_otp: str,
    amount: int,
    message: str,
):
    payment = OMPayment(phonenumber, username, password)
    return payment.validate_payment(customer_phone, customer_otp, amount, message)


def validate_om_dev_payment(
    username: str,
    password: str,
    phonenumber: str,
    customer_phone: str,
    customer_otp: str,
    amount: int,
    message: str,
):
    payment = OMDevPayment(phonenumber, username, password)
    return payment.validate_payment(customer_phone, customer_otp, amount, message)
