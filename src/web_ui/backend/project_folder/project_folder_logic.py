import os

from src.web_ui.backend import api_models


def deduce_containing_project_folder(
        abs_source_path: str,
        all_project_folders: list[api_models.ProjectFolder],
) -> api_models.ProjectFolder | None:
    """
    Given a source_path, find the project folder that contains it.
    """
    for project_folder in all_project_folders:
        if abs_source_path.startswith(os.path.expanduser(project_folder.logical_path)):
            return project_folder
    return None
