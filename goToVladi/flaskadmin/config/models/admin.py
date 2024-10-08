from dataclasses import dataclass
from enum import Enum


class TemplateMode(str, Enum):
    bootstrap2 = "bootstrap2"
    bootstrap3 = "bootstrap3"
    bootstrap4 = "bootstrap4"


@dataclass
class FlaskAdminConfig:
    template_mode: TemplateMode = TemplateMode.bootstrap4
    media_url: str = "/media"
    static_path: str = "/static"
