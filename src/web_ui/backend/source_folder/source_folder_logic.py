import os
from pathlib import Path


def deduce_abs_source_path(
    abs_or_rel_source_path: str,
    selected_project_folder: str | None,
) -> str | None:
    abs_source_path: str
    if abs_or_rel_source_path.startswith("~"):
        abs_source_path = os.path.expanduser(abs_or_rel_source_path)
    elif abs_or_rel_source_path.startswith("/"):
        abs_source_path = abs_or_rel_source_path
    elif selected_project_folder is not None:
        abs_source_path = os.path.join(os.path.expanduser(selected_project_folder), abs_or_rel_source_path)
    else:
        return None
    return abs_source_path


def deduce_nearest_existing_source_path(
    abs_source_path: str,
) -> str | None:
    p = Path(abs_source_path)
    while True:
        if p.exists():
            return str(p)
        if len(p.parts) == 1:
            return None
        p = p.parent
