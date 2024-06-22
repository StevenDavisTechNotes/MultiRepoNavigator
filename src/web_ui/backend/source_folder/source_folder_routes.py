# cSpell: ignore fastapi

import os
import re

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.language import SOURCE_CODE_EXTENSIONS, LanguageType

from src.web_ui.backend import api_models, db_models
from src.web_ui.backend.database import get_db_session
from src.web_ui.backend.project_folder.project_folder_logic import \
    deduce_containing_project_folder
from src.web_ui.backend.source_folder.source_folder_logic import (
    deduce_abs_source_path, deduce_nearest_existing_source_path)

router = APIRouter(
    prefix="/source_code",
    tags=["source_code"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/list_code_files", response_model=api_models.ListCodeFilesResponse,)
def list_code_files(
        abs_or_rel_source_path: str = "m",
        selected_project_folder: str | None = "~\\src\\py_repo_1",
        db_session: Session = Depends(get_db_session),
) -> api_models.ListCodeFilesResponse | api_models.ListCodeFilesErrorResponse:
    all_project_folders: list[api_models.ProjectFolder] = [
        db_models.convert_project_folder_db_to_api(x)
        for x in db_session.query(db_models.ProjectFolder).all()
    ]

    abs_source_path = deduce_abs_source_path(
        abs_or_rel_source_path=abs_or_rel_source_path,
        selected_project_folder=selected_project_folder,
    )
    if abs_source_path is None:
        return api_models.ListCodeFilesErrorResponse(
            message="source_path must be absolute or relative to selected_project_folder",
            partial_source_path=abs_or_rel_source_path,
            project_folder=None,
        )

    project_folder = deduce_containing_project_folder(
        abs_source_path=abs_source_path,
        all_project_folders=all_project_folders,
    )
    if project_folder is None:
        return api_models.ListCodeFilesErrorResponse(
            message=f"Unknown project folder for {abs_source_path}",
            partial_source_path=abs_or_rel_source_path,
            project_folder=None,
        )

    project_path = os.path.expanduser(project_folder.logical_path)
    nearest_parent_source_path = (
        deduce_nearest_existing_source_path(abs_source_path)
        or project_path)
    extension_regex = form_regex_for_language(project_folder.language)
    code_file_paths: list[str] = []
    for root, _dirs, files in os.walk(nearest_parent_source_path):
        for name in files:
            abs_file_path = os.path.join(root, name)
            if not abs_file_path.startswith(abs_source_path):
                continue
            if extension_regex.search(abs_file_path) is None:
                continue
            if len(code_file_paths) >= 100:
                break
            code_file_paths.append(os.path.relpath(abs_file_path, project_path))
    return api_models.ListCodeFilesResponse(
        project_folder=project_folder,
        code_file_paths=code_file_paths,
    )


def form_regex_for_language(language: str) -> re.Pattern[str]:
    if language.lower() not in LanguageType:
        raise ValueError(f"Unknown language {language}")
    project_language = LanguageType(language)
    if project_language not in SOURCE_CODE_EXTENSIONS:
        raise ValueError(f"Missing an extension lists for {language}")
    extension_list = SOURCE_CODE_EXTENSIONS[project_language]
    extension_pattern_list = [x.replace('.', '') for x in extension_list]
    pattern = r"\.(" + "|".join(extension_pattern_list) + ")$"
    extension_regex = re.compile(pattern)
    return extension_regex
