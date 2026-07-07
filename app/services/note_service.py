from app.repositories.log_repository import LogRepository
from app.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self, note_repository: NoteRepository, log_repository: LogRepository):
        self.note_repository = note_repository
        self.log_repository = log_repository

    def create(self, title: str, content: str):
        note = self.note_repository.create(title=title, content=content)
        self.log_repository.create(action="create", target="note", target_id=note["id"], details=title)
        return note

    def list_all(self):
        return self.note_repository.list_all()

    def update(self, note_id: int, title: str, content: str):
        note = self.note_repository.update(note_id=note_id, title=title, content=content)
        if note:
            self.log_repository.create(action="update", target="note", target_id=note_id, details=title)
        return note

    def delete(self, note_id: int):
        deleted = self.note_repository.delete(note_id)
        if deleted:
            self.log_repository.create(action="delete", target="note", target_id=note_id)
        return deleted
