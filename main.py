from mobilemoney import validate_om_prod_payment


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
