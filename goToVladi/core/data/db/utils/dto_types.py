from typing import Annotated, Union

from phonenumbers import PhoneNumber
from pydantic_extra_types.phone_numbers import PhoneNumberValidator

PhoneNumberType = Annotated[
    Union[str, PhoneNumber],
    PhoneNumberValidator(
        supported_regions=["RU"], default_region="RU",
        number_format="INTERNATIONAL"
    )
]
