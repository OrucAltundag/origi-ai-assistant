from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Origi Assistant")
    db_path: str = os.getenv("DB_PATH", "origi.db")


settings = Settings()
