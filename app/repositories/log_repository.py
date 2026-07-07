from app.db.database import get_connection, utc_now_iso


class LogRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create(self, action: str, target: str, target_id: int | None = None, details: str | None = None) -> None:
        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO action_logs(action, target, target_id, details, created_at)
                VALUES(?, ?, ?, ?, ?)
                """,
                (action, target, target_id, details, utc_now_iso()),
            )

    def list_recent(self, limit: int = 100):
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                "SELECT id, action, target, target_id, details, created_at FROM action_logs ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
