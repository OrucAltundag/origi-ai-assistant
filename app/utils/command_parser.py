import re


COMMAND_PATTERNS = [
    (r"^(?:create|add) note (?P<title>[^:]+):(?P<content>.+)$", "create_note"),
    (r"^(?:list|show) notes$", "list_notes"),
    (r"^(?:create|add) task (?P<title>.+)$", "create_task"),
    (r"^(?:list|show) tasks$", "list_tasks"),
    (r"^(?:complete|finish) task (?P<id>\d+)$", "complete_task"),
    (r"^(?:delete|remove) note (?P<id>\d+)$", "delete_note"),
    (r"^(?:delete|remove) task (?P<id>\d+)$", "delete_task"),
]


def parse_command(command: str) -> tuple[str, dict]:
    normalized = command.strip()
    for pattern, intent in COMMAND_PATTERNS:
        match = re.match(pattern, normalized, flags=re.IGNORECASE)
        if match:
            payload = {key: value.strip() for key, value in match.groupdict().items()}
            if "id" in payload:
                payload["id"] = int(payload["id"])
            return intent, payload
    raise ValueError("Unsupported command format")
