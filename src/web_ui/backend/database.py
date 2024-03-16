import datetime
import os

import pytz
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker as session_maker

# cSpell: ignore sessionmaker
from src.utils.file_handling import (absolute_to_user_relative_path,
                                     mkdir_if_not_exists, remove_file_if_exists)
from src.web_ui.backend import db_models
from src.web_ui.backend.config import ROOT_DATA_PATH

DATABASE_FILE_PATH = os.path.join(ROOT_DATA_PATH, "multi_repo_navigator.db")
remove_file_if_exists(DATABASE_FILE_PATH)  # just for initial testing
DATABASE_NEEDS_SCHEMA = not os.path.exists(DATABASE_FILE_PATH)

# Create a sqlite engine instance
mkdir_if_not_exists(ROOT_DATA_PATH)
engine: Engine = create_engine("sqlite:///" + DATABASE_FILE_PATH)

# Create SessionLocal class from sessionmaker factory
SessionLocal = session_maker(bind=engine, expire_on_commit=False)


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def initialize_database():
    # Upsert tables
    db_models.Base.metadata.create_all(engine)  # type: ignore
    if not DATABASE_NEEDS_SCHEMA:
        return
    # Seed data
    for session in get_db_session():
        last_used = datetime.datetime.now().astimezone(pytz.utc)
        session.add(db_models.ProjectFolder(
            app_name="py_repo_1",
            language="python",
            last_used=last_used,
            logical_path=absolute_to_user_relative_path(
                os.path.join("~", "src", "py_repo_1")),
        ))
        session.add(db_models.ProjectFolder(
            app_name="py_repo_2",
            language="python",
            last_used=last_used,
            logical_path=absolute_to_user_relative_path(
                os.path.join("~", "src", "py_repo_2")),
        ))
        session.commit()
