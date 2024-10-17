from pathlib import Path


def get_relative_path(file_path: Path | str, media_path: Path) -> Path:
    if isinstance(file_path, str):
        file_path = Path(file_path).resolve()
    if not file_path.is_relative_to(media_path):
        raise ValueError(
            f"Media root `{media_path.as_posix()}` "
            f"is not parent path for file `{file_path.as_posix()}"
        )
    return file_path.relative_to(media_path)
