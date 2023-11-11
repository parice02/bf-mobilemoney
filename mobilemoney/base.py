from typing import Any, List, Union, Dict


class BasePayment(object):
    """ """

    def __init__(self, phonenumber: str = "", username: str = "", password: str = ""):
        if not isinstance(phonenumber, str):
            raise ValueError("value 'phonenumber' must be type of 'str'")

        if not isinstance(username, str):
            raise ValueError("value 'username' must be type of 'str'")

        if not isinstance(password, str):
            raise ValueError("value 'username' must be type of 'str'")

        self._username = username
        self._password = password
        self._phonenumber = phonenumber

    @property
    def phonenumber(self):
        return self._phonenumber

    @phonenumber.setter
    def phonenumber(self, value):
        self._phonenumber = value

    @phonenumber.deleter
    def phonenumber(self):
        del self._phonenumber

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @username.deleter
    def username(self):
        del self._username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @password.deleter
    def password(self):
        del self._password
