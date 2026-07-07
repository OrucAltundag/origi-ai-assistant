import os
import tempfile
import unittest

from app.db.database import init_db
from app.repositories.log_repository import LogRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.task_repository import TaskRepository
from app.services.command_service import CommandService
from app.services.note_service import NoteService
from app.services.task_service import TaskService
from app.utils.command_parser import parse_command
from app.utils.confirmation import require_confirmation
from fastapi import HTTPException


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tempdir.name, "test.db")
        init_db(self.db_path)

        log_repository = LogRepository(self.db_path)
        self.note_service = NoteService(NoteRepository(self.db_path), log_repository)
        self.task_service = TaskService(TaskRepository(self.db_path), log_repository)
        self.command_service = CommandService(self.note_service, self.task_service)
        self.log_repository = log_repository

    def tearDown(self):
        self.tempdir.cleanup()

    def test_note_lifecycle_and_logs(self):
        note = self.note_service.create("meeting", "summary")
        self.assertEqual(note["title"], "meeting")

        updated = self.note_service.update(note["id"], "meeting-2", "summary-2")
        self.assertEqual(updated["title"], "meeting-2")

        deleted = self.note_service.delete(note["id"])
        self.assertTrue(deleted)

        logs = self.log_repository.list_recent(limit=5)
        self.assertEqual([log["action"] for log in logs[:3]], ["delete", "update", "create"])

    def test_task_complete(self):
        task = self.task_service.create("ship mvp", "")
        completed = self.task_service.complete(task["id"])
        self.assertTrue(completed["completed"])

    def test_confirmation_guard(self):
        with self.assertRaises(HTTPException):
            require_confirmation(False)

    def test_command_parser_and_execution(self):
        intent, payload = parse_command("create note plan: finish sprint")
        self.assertEqual(intent, "create_note")
        self.assertEqual(payload["title"], "plan")

        intent, payload, result = self.command_service.execute("create task ship")
        self.assertEqual(intent, "create_task")
        self.assertEqual(payload["title"], "ship")
        self.assertEqual(result["title"], "ship")


if __name__ == "__main__":
    unittest.main()
