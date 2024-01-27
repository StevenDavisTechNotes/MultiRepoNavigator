
from pathlib import Path
import shutil
import os


def absolute_to_user_relative_path(abs_file_path: str) -> str:
    home_path = os.path.expanduser("~")
    if abs_file_path.startswith(home_path):
        return os.path.join("~", os.path.relpath(abs_file_path, home_path))
    else:
        return abs_file_path


def remove_file_if_exists(path: str):
    if os.path.exists(path):
        os.remove(path)


def mkdir_if_not_exists(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def make_parent_dir_if_not_exists(path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def delete_folder_with_files(dir_path: str):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
