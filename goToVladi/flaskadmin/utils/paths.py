from pathlib import Path


def get_relative_path(file_path: Path, root_path: Path) -> Path:
    file_parts = list(file_path.parts)
    for i, root_part in enumerate(root_path.parts):
        if file_parts[i] == root_part:
            file_parts[i] = None
        else:
            break
    return Path(*filter(lambda x: x is not None, file_parts))
