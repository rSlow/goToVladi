from dataclasses import dataclass


@dataclass
class FlaskStaticConfig:
    path: str
    scss_output_style: str = "nested"
