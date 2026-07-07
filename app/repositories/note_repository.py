from app.db.database import get_connection, utc_now_iso


class NoteRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create(self, title: str, content: str):
        now = utc_now_iso()
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO notes(title, content, created_at, updated_at)
                VALUES(?, ?, ?, ?)
                """,
                (title, content, now, now),
            )
            note_id = cursor.lastrowid
            return self._get_with_connection(connection, note_id)

    def list_all(self):
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                "SELECT id, title, content, created_at, updated_at FROM notes ORDER BY id DESC"
            )
            return [dict(row) for row in cursor.fetchall()]

    def get(self, note_id: int):
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, note_id: int, title: str, content: str):
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                """
                UPDATE notes
                SET title = ?, content = ?, updated_at = ?
                WHERE id = ?
                """,
                (title, content, utc_now_iso(), note_id),
            )
            if cursor.rowcount == 0:
                return None
            return self._get_with_connection(connection, note_id)

    def delete(self, note_id: int) -> bool:
        with get_connection(self.db_path) as connection:
            cursor = connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            return cursor.rowcount > 0

    @staticmethod
    def _get_with_connection(connection, note_id: int):
        cursor = connection.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?",
            (note_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None
