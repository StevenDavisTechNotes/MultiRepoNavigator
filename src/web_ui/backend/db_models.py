import datetime
from dataclasses import asdict, dataclass

from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import declarative_base

from src.web_ui.backend import api_models

Base = declarative_base()

# pyright: reportGeneralTypeIssues=false


@dataclass
class ProjectFolder(Base):
    __tablename__ = 'project_folder'
    id: int = Column(Integer, primary_key=True)  # pyright: ignore[reportAssignmentType]
    app_name: str = Column(String(256))  # pyright: ignore[reportAssignmentType]
    language: str = Column(String(256))  # pyright: ignore[reportAssignmentType]
    last_used: datetime.datetime = Column(TIMESTAMP)  # pyright: ignore[reportAssignmentType]
    logical_path: str = Column(String(256))  # pyright: ignore[reportAssignmentType]


@dataclass
class FuncDefFav(Base):
    __tablename__ = 'func_def_fav'
    id: int = Column(Integer, primary_key=True)  # pyright: ignore[reportAssignmentType]
    function_name: str = Column(String(256))  # pyright: ignore[reportAssignmentType]
    last_used: datetime.datetime = Column(TIMESTAMP)  # pyright: ignore[reportAssignmentType]
    resolved_path: str = Column(String(256))  # pyright: ignore[reportAssignmentType]


@dataclass
class Todo(Base):
    __tablename__ = 'todo'
    id: int = Column(Integer, primary_key=True)  # pyright: ignore[reportAssignmentType]
    category: str = Column(String(256))  # pyright: ignore[reportAssignmentType]
    logical_path: str = Column(String(256))  # pyright: ignore[reportAssignmentType]
    line_number: int = Column(Integer)  # pyright: ignore[reportAssignmentType]


def convert_project_folder_db_to_api(db_model: ProjectFolder) -> api_models.ProjectFolder:
    return api_models.ProjectFolder(**asdict(db_model))


def convert_func_def_fav_db_to_api(db_model: FuncDefFav) -> api_models.FuncDefFav:
    return api_models.FuncDefFav(**asdict(db_model))
