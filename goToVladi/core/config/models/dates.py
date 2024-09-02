from dataclasses import dataclass


@dataclass
class DatesConfig:
    date_format: str
    time_format: str
    datetime_format: str
