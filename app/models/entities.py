from dataclasses import dataclass


@dataclass
class Note:
    id: int
    title: str
    content: str
    created_at: str
    updated_at: str


@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str


@dataclass
class ActionLog:
    id: int
    action: str
    target: str
    target_id: int | None
    details: str | None
    created_at: str
