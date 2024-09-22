from dataclasses import dataclass


@dataclass
class WebConfig:
    base_url: str
    root_path: str | None = None

    @property
    def real_base_url(self):
        res = self.base_url
        if self.root_path:
            res += self.root_path
        return res
