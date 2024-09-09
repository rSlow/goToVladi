from sqlalchemy_utils import PhoneNumberType, PhoneNumber


class StringPhoneNumberType(PhoneNumberType):
    python_type = str

    def process_result_value(self, value, dialect):
        if value:
            phone = PhoneNumber(value, self.region)
            return phone.e164
        return value
