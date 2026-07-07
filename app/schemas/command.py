from typing import Any

from pydantic import BaseModel, Field


class CommandRequest(BaseModel):
    command: str = Field(min_length=1)


class CommandResponse(BaseModel):
    intent: str
    payload: dict[str, Any]
    executed: bool = False
    result: dict[str, Any] | list[dict[str, Any]] | None = None
