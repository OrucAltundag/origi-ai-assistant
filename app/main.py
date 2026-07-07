from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import build_router
from app.core.config import settings
from app.db.database import init_db
from app.repositories.log_repository import LogRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.task_repository import TaskRepository
from app.services.command_service import CommandService
from app.services.note_service import NoteService
from app.services.task_service import TaskService


def create_app() -> FastAPI:
    init_db(settings.db_path)

    note_repository = NoteRepository(settings.db_path)
    task_repository = TaskRepository(settings.db_path)
    log_repository = LogRepository(settings.db_path)

    note_service = NoteService(note_repository, log_repository)
    task_service = TaskService(task_repository, log_repository)
    command_service = CommandService(note_service, task_service)

    app = FastAPI(title=settings.app_name)
    app.include_router(build_router(note_service, task_service, command_service), prefix="/api")

    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/", include_in_schema=False)
    def serve_frontend():
        return FileResponse(frontend_dir / "index.html")

    return app


app = create_app()
