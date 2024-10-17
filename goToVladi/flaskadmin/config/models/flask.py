from dataclasses import dataclass


@dataclass
class FlaskConfig:
    secret_key: str
    root_path: str = "/admin"
    debug: bool = False

    def get_real_root_path(self, base_root_path: str | None) -> str | None:
        if self.root_path or base_root_path:
            return (base_root_path or "") + self.root_path
