import os


def compute_module_name(abs_file_path: str, project_root_path: str) -> str:
    return ".".join(abs_file_path.split(os.sep))
