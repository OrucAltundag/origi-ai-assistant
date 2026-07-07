from app.db.database import get_connection, utc_now_iso


class TaskRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create(self, title: str, description: str = ""):
        now = utc_now_iso()
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks(title, description, completed, created_at, updated_at)
                VALUES(?, ?, 0, ?, ?)
                """,
                (title, description, now, now),
            )
            task_id = cursor.lastrowid
            row = self._get_with_connection(connection, task_id)
            return self._normalize(dict(row)) if row else None

    def list_all(self):
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                "SELECT id, title, description, completed, created_at, updated_at FROM tasks ORDER BY id DESC"
            )
            return [self._normalize(dict(row)) for row in cursor.fetchall()]

    def get(self, task_id: int):
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                "SELECT id, title, description, completed, created_at, updated_at FROM tasks WHERE id = ?",
                (task_id,),
            )
            row = cursor.fetchone()
            return self._normalize(dict(row)) if row else None

    def update(self, task_id: int, title: str, description: str = ""):
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, updated_at = ?
                WHERE id = ?
                """,
                (title, description, utc_now_iso(), task_id),
            )
            if cursor.rowcount == 0:
                return None
            row = self._get_with_connection(connection, task_id)
            return self._normalize(dict(row)) if row else None

    def mark_complete(self, task_id: int):
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET completed = 1, updated_at = ?
                WHERE id = ?
                """,
                (utc_now_iso(), task_id),
            )
            if cursor.rowcount == 0:
                return None
            row = self._get_with_connection(connection, task_id)
            return self._normalize(dict(row)) if row else None

    def delete(self, task_id: int) -> bool:
        with get_connection(self.db_path) as connection:
            cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    @staticmethod
    def _normalize(task: dict):
        task["completed"] = bool(task["completed"])
        return task

    @staticmethod
    def _get_with_connection(connection, task_id: int):
        cursor = connection.execute(
            "SELECT id, title, description, completed, created_at, updated_at FROM tasks WHERE id = ?",
            (task_id,),
        )
        return cursor.fetchone()
