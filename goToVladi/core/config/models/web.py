from dataclasses import dataclass


@dataclass
class WebConfig:
    base_url: str

    def get_real_base_url(self, root_path: str | None = None) -> str:
        return self.base_url + root_path \
            if root_path is not None \
            else self.base_url
