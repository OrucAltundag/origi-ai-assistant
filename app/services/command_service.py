from app.services.note_service import NoteService
from app.services.task_service import TaskService
from app.utils.command_parser import parse_command


class CommandService:
    def __init__(self, note_service: NoteService, task_service: TaskService):
        self.note_service = note_service
        self.task_service = task_service

    def parse(self, command: str):
        return parse_command(command)

    def execute(self, command: str):
        intent, payload = parse_command(command)

        if intent == "create_note":
            result = self.note_service.create(title=payload["title"], content=payload["content"])
        elif intent == "list_notes":
            result = self.note_service.list_all()
        elif intent == "create_task":
            result = self.task_service.create(title=payload["title"])
        elif intent == "list_tasks":
            result = self.task_service.list_all()
        elif intent == "complete_task":
            result = self.task_service.complete(task_id=payload["id"])
        elif intent == "delete_note":
            result = {"deleted": self.note_service.delete(note_id=payload["id"]) }
        elif intent == "delete_task":
            result = {"deleted": self.task_service.delete(task_id=payload["id"]) }
        else:
            raise ValueError("Unsupported command")

        return intent, payload, result
