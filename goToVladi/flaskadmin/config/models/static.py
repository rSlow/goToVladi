from dataclasses import dataclass


@dataclass
class FlaskStaticConfig:
    base_url: str
    scss_output_style: str = "compressed"
