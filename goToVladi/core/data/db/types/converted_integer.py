from sqlalchemy import TypeDecorator, Integer


class ConvertedInteger(TypeDecorator):
    """
    This is fix for fastadmin, which try to save id of related object as
    string value. This type decorator try to convert value to integer.
    """

    impl = Integer
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return int(value)

    def process_result_value(self, value, dialect):
        return value
