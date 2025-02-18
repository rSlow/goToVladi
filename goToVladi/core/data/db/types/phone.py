from sqlalchemy_utils import PhoneNumberType as BasePhoneNumberType


class PhoneNumberType(BasePhoneNumberType):
    def process_bind_param(self, value, dialect):
        if not value:
            return None
        return super().process_bind_param(value, dialect)

    def process_result_value(self, value, dialect):
        if not value:
            return None
        return super().process_result_value(value, dialect)
