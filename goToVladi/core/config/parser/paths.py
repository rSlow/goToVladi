from pathlib import Path

from ..models.paths import Paths


def get_paths(env_var: str | None = None) -> Paths:  # TODO env_path_var
    # if path := os.getenv(env_var):
    #     return Paths(Path(path))
    return Paths(Path(__file__).parent.parent.parent.parent.parent)
