from fastapi import APIRouter, HTTPException, status

from app.schemas.command import CommandRequest, CommandResponse
from app.schemas.note import NoteCreate, NoteOut, NoteUpdate
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.command_service import CommandService
from app.services.note_service import NoteService
from app.services.task_service import TaskService
from app.utils.confirmation import require_confirmation


def build_router(note_service: NoteService, task_service: TaskService, command_service: CommandService) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health_check():
        return {"status": "ok"}

    @router.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
    def create_note(payload: NoteCreate):
        return note_service.create(title=payload.title, content=payload.content)

    @router.get("/notes", response_model=list[NoteOut])
    def list_notes():
        return note_service.list_all()

    @router.put("/notes/{note_id}", response_model=NoteOut)
    def update_note(note_id: int, payload: NoteUpdate):
        note = note_service.update(note_id=note_id, title=payload.title, content=payload.content)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        return note

    @router.delete("/notes/{note_id}")
    def delete_note(note_id: int, confirm: bool = False):
        require_confirmation(confirm)
        deleted = note_service.delete(note_id=note_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        return {"deleted": True}

    @router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
    def create_task(payload: TaskCreate):
        return task_service.create(title=payload.title, description=payload.description)

    @router.get("/tasks", response_model=list[TaskOut])
    def list_tasks():
        return task_service.list_all()

    @router.put("/tasks/{task_id}", response_model=TaskOut)
    def update_task(task_id: int, payload: TaskUpdate):
        task = task_service.update(task_id=task_id, title=payload.title, description=payload.description)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    @router.patch("/tasks/{task_id}/complete", response_model=TaskOut)
    def complete_task(task_id: int):
        task = task_service.complete(task_id=task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    @router.delete("/tasks/{task_id}")
    def delete_task(task_id: int, confirm: bool = False):
        require_confirmation(confirm)
        deleted = task_service.delete(task_id=task_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return {"deleted": True}

    @router.post("/commands", response_model=CommandResponse)
    def parse_or_execute_command(payload: CommandRequest):
        try:
            intent, parsed_payload, result = command_service.execute(payload.command)
            return CommandResponse(intent=intent, payload=parsed_payload, executed=True, result=result)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return router
