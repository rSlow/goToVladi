from dataclasses import dataclass


@dataclass
class FlaskConfig:
    secret_key: str
    root_path: str = ""
