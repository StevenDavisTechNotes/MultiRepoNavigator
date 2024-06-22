# cSpell: ignore uvicorn

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.web_ui.backend.database import initialize_database
from src.web_ui.backend.function_head.function_head_routes import \
    router as func_def_fav_router
from src.web_ui.backend.function_impl.function_impl_routes import \
    router as function_impl_router
from src.web_ui.backend.project_folder.project_folder_routes import \
    router as project_folder_routes
from src.web_ui.backend.source_folder.source_folder_routes import \
    router as source_folder_router

# pre-app steps
initialize_database()

# Initialize app
app = FastAPI()

origins = [
    "http://localhost:4060",
    "localhost:4060"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(project_folder_routes)
app.include_router(source_folder_router)
app.include_router(func_def_fav_router)
app.include_router(function_impl_router)


@app.get("/")
def root():
    return "WebUI"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4059)
