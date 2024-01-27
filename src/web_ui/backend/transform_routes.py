
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.web_ui.backend import api_models, db_models
from src.web_ui.backend.database import get_db_session

router = APIRouter(
    prefix="/transform",
    tags=["transform"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/isolate_function", response_model=api_models.ProjectFolder, status_code=status.HTTP_201_CREATED)
def create(
        item: api_models.ProjectFolderCreate,
        session: Session = Depends(get_db_session),
) -> api_models.ProjectFolder:

    db_model = db_models.ProjectFolder(
        last_used=item.last_used,
        logical_path=item.logical_path,
        app_name=item.app_name,
    )
    session.add(db_model)
    session.commit()
    session.refresh(db_model)

    return api_models.ProjectFolder(**db_model.__dict__)
