import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.web_ui.backend import api_models, db_models
from src.web_ui.backend.database import get_db_session

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/project_folder",
    tags=["project_folder"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=api_models.ProjectFolder, status_code=status.HTTP_201_CREATED)
def create(
        item: api_models.ProjectFolderCreate,
        session: Session = Depends(get_db_session),
) -> api_models.ProjectFolder:
    logger.info(f"creating {item}")

    db_model = db_models.ProjectFolder(
        last_used=item.last_used,
        logical_path=item.logical_path,
        app_name=item.app_name,
    )
    session.add(db_model)
    session.commit()
    session.refresh(db_model)

    return db_models.convert_project_folder_db_to_api(db_model)


@router.get("/{id}", response_model=api_models.ProjectFolder)
def read(
        id: int,
        session: Session = Depends(get_db_session),
) -> api_models.ProjectFolder:
    logger.info(f"reading {id}")

    db_model = session.query(db_models.ProjectFolder).get(id)

    if not db_model:
        raise HTTPException(
            status_code=404, detail=f"ProjectFolder with id {id} not found")

    return db_models.convert_project_folder_db_to_api(db_model)


@router.patch("/{id}", response_model=bool)
def patch(
        id: int,
        request: api_models.ProjectFolderPatch,
        session: Session = Depends(get_db_session),
) -> bool:
    logger.info(f"patching {id} with {request}")
    patch: dict[str, str | datetime.datetime] = request.model_dump(
        exclude_unset=True)
    del patch["id"]
    num_rows_updated = (
        session
        .query(db_models.ProjectFolder)
        .filter_by(id=id)
        .update(patch)
    )
    session.commit()
    return True if num_rows_updated == 1 else False


@router.put("/{id}", response_model=api_models.ProjectFolder)
def update(
        id: int,
        request: api_models.ProjectFolder,
        session: Session = Depends(get_db_session),
) -> api_models.ProjectFolder:
    logger.info(f"update {id} with {request}")
    db_model = session.query(db_models.ProjectFolder).get(id)

    if db_model:
        db_model.logical_path = request.logical_path
        db_model.last_used = request.last_used
        db_model.app_name = request.app_name
        session.commit()

    if not db_model:
        raise HTTPException(
            status_code=404, detail=f"ProjectFolder with id {id} not found")

    return db_models.convert_project_folder_db_to_api(db_model)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
        id: int,
        session: Session = Depends(get_db_session),
) -> None:
    logger.info(f"delete {id}")
    db_model = session.query(db_models.ProjectFolder).get(id)

    if db_model:
        session.delete(db_model)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"ProjectFolder with id {id} not found")

    return None


@router.get("/", response_model=list[api_models.ProjectFolder])
def index(
        session: Session = Depends(get_db_session),
) -> list[api_models.ProjectFolder]:
    logger.info("index")

    items: list[db_models.ProjectFolder] = session.query(
        db_models.ProjectFolder).all()

    return [db_models.convert_project_folder_db_to_api(x) for x in items]
