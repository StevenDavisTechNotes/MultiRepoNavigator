import datetime

from pydantic import BaseModel


class ProjectFolderCreate(BaseModel):
    logical_path: str
    app_name: str
    last_used: datetime.datetime


class ProjectFolder(BaseModel):
    id: int
    app_name: str
    language: str
    last_used: datetime.datetime
    logical_path: str


class ProjectFolderPatch(BaseModel):
    id: int
    last_used: datetime.datetime | None = None
    logical_path: str | None = None
    app_name: str | None = None


class FuncDefFavCreate(BaseModel):
    function_name: str
    last_used: datetime.datetime
    resolved_path: str


class FuncDefFav(BaseModel):
    id: int
    function_name: str
    last_used: datetime.datetime
    resolved_path: str


class ListCodeFilesErrorResponse(BaseModel):
    message: str
    partial_source_path: str
    project_folder: str | None


class ListCodeFilesResponse(BaseModel):
    project_folder: ProjectFolder
    code_file_paths: list[str]


class ExtractedFunctionFromSourceRequest(BaseModel):
    function_declaration_statement: str
    headers_start: int
    headers_end: int
    body_start: int
    body_end: int
    is_isolated: bool
    is_multi_head: bool


class ExtractFunctionsFromSourceResponse(BaseModel):
    module_statement: str
    import_statements: list[str]
    functions: list[ExtractedFunctionFromSourceRequest]


# class IsolationFunctionRequest(BaseModel):
#     function: Optional[str] = None
#     module_statement: str
#     import_statements: list[str]
#     function_text: str
#     source_path: str
