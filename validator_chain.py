from abc import abstractmethod
from datetime import datetime
import re

class ValidatorChain:

    @abstractmethod
    def set_next(self, validator_chain: "ValidatorChain") -> "ValidatorChain":
        pass

    @abstractmethod
    def validate(self, string: str):
        pass

class FieldTypeValidator(ValidatorChain):

    _next_validator: ValidatorChain = None

    def set_next(self, validator_chain: ValidatorChain) -> ValidatorChain:
        self._next_validator = validator_chain
        return validator_chain

    @abstractmethod
    def validate(self, string: str) -> str:
        if self._next_validator:
            return self._next_validator.validate(string)

        return "TEXT"

class DateValidator(FieldTypeValidator):

    formats = ["%d.%m.%Y", "%Y-%m-%d"]

    def check_format(self, date: str, form: str) -> bool:
        try:
            datetime.strptime(date, form)
        except ValueError:
            return False

        return True

    def is_date(self, date: str) -> bool:
        return any(self.check_format(date, form) for form in self.formats)

    def validate(self, string: str) -> str:
        if not self.is_date(string):
            return super().validate(string)

        return "DATE"

class PhoneValidator(FieldTypeValidator):

    __PHONE_REGEX = re.compile(r"\+7 \d{3} \d{3} \d{2} \d{2}") 

    def is_phone(self, phone: str) -> bool:
        return bool(self.__PHONE_REGEX.fullmatch(phone))

    def validate(self, string: str) -> str:
        if not self.is_phone(string):
            return super().validate(string)

        return "PHONE"

class EmailValidator(FieldTypeValidator):

    __EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}")

    def is_email(self, email: str) -> bool:
        return bool(self.__EMAIL_REGEX.fullmatch(email))

    def validate(self, string: str) -> str:
        if not self.is_email(string):
            return super().validate(string)

        return "EMAIL"

