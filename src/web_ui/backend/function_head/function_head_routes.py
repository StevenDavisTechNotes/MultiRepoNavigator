from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.web_ui.backend import api_models, db_models
from src.web_ui.backend.database import get_db_session

router = APIRouter(
    prefix="/function_head",
    tags=["function_head"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=api_models.FuncDefFav, status_code=status.HTTP_201_CREATED)
def create(
        item: api_models.FuncDefFavCreate,
        session: Session = Depends(get_db_session),
) -> api_models.FuncDefFav:

    db_model = db_models.FuncDefFav(
        function_name=item.function_name,
        last_used=item.last_used,
        resolved_path=item.resolved_path,
    )
    session.add(db_model)
    session.commit()
    session.refresh(db_model)

    # pyright: ignore[reportGeneralTypeIssues]
    return db_models.convert_func_def_fav_db_to_api(db_model)


@router.get("/{id}", response_model=api_models.FuncDefFav)
def read(
        id: int,
        session: Session = Depends(get_db_session),
) -> api_models.FuncDefFav:

    db_model = session.query(db_models.FuncDefFav).get(id)

    if not db_model:
        raise HTTPException(
            status_code=404, detail=f"FuncDefFav with id {id} not found")

    return db_models.convert_func_def_fav_db_to_api(db_model)


@router.put("/{id}", response_model=api_models.FuncDefFav)
def update(
        id: int,
        logical_path: str,
        app_name: str,
        session: Session = Depends(get_db_session),
) -> api_models.FuncDefFav:
    db_model = session.query(db_models.FuncDefFav).get(id)

    if db_model:
        db_model.logical_path = logical_path
        db_model.app_name = app_name
        session.commit()

    if not db_model:
        raise HTTPException(
            status_code=404, detail=f"FuncDefFav with id {id} not found")

    return db_models.convert_func_def_fav_db_to_api(db_model)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
        id: int,
        session: Session = Depends(get_db_session),
) -> None:

    db_model = session.query(db_models.FuncDefFav).get(id)

    if db_model:
        session.delete(db_model)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"FuncDefFav with id {id} not found")

    return None


@router.get("/", response_model=list[api_models.FuncDefFav])
def index(
        session: Session = Depends(get_db_session),
) -> list[api_models.FuncDefFav]:
    items = session.query(db_models.FuncDefFav).all()
    return [db_models.convert_func_def_fav_db_to_api(x) for x in items]
