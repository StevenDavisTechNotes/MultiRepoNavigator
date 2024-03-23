
import os
import re

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.language import SOURCE_CODE_EXTENTIONS, LanguageType

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

    nearest_parent_source_path = (
        deduce_nearest_existing_source_path(abs_source_path)
        or os.path.expanduser(project_folder.logical_path))
    extention_regex = form_regex_for_language(project_folder.language)
    code_file_paths: list[str] = [
        abs_file_path
        for root, _dirs, files in os.walk(nearest_parent_source_path)
        for name in files
        if (abs_file_path := os.path.join(root, name))
        if abs_file_path.startswith(abs_source_path)
        if extention_regex.search(abs_file_path) is not None
    ]
    return api_models.ListCodeFilesResponse(
        project_folder=project_folder,
        code_file_paths=code_file_paths[:100],
    )


def form_regex_for_language(language: str) -> re.Pattern[str]:
    if language.lower() not in LanguageType:
        raise ValueError(f"Unknown language {language}")
    project_language = LanguageType(language)
    if project_language not in SOURCE_CODE_EXTENTIONS:
        raise ValueError(f"Missing an extention lists for {language}")
    extension_list = SOURCE_CODE_EXTENTIONS[project_language]
    extension_pattern_list = [x.replace('.', '') for x in extension_list]
    pattern = r"\.(" + "|".join(extension_pattern_list) + ")$"
    extention_regex = re.compile(pattern)
    return extention_regex
