from dataclasses import dataclass


@dataclass
class WebhookConfig:
    web_url: str
    path: str
    secret: str
