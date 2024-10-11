from dataclasses import dataclass
from enum import Enum


class TemplateMode(str, Enum):
    bootstrap2 = "bootstrap2"
    bootstrap3 = "bootstrap3"
    bootstrap4 = "bootstrap4"


@dataclass
class FlaskAdminConfig:
    media_url: str
    template_mode: TemplateMode = TemplateMode.bootstrap4
