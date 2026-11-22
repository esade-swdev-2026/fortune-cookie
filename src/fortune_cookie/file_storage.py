import json
from dataclasses import asdict
from pathlib import Path

from fortune_cookie.fortune_rules import Fortune

data_dir = Path.cwd() / "data"

history_file = data_dir / ".fortune_cookie_history.json"
last_message_file = data_dir / ".fortune_cookie_last.txt"
custom_messages_file = data_dir / ".fortune_cookie_messages.json"


def load_history() -> set[str]:
    if not history_file.exists():
        return set()

    with open(history_file, encoding="utf-8") as file:
        saved_messages = json.load(file)

    return set(saved_messages)


def save_history(seen_messages: set[str]) -> None:
    history_file.parent.mkdir(parents=True, exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(sorted(seen_messages), file)


def load_last_message() -> str | None:
    if not last_message_file.exists():
        return None

    return last_message_file.read_text(encoding="utf-8")


def save_last_message(message: str) -> None:
    last_message_file.parent.mkdir(parents=True, exist_ok=True)
    last_message_file.write_text(message, encoding="utf-8")


def save_custom_messages(custom_messages: list[Fortune]) -> None:
    custom_messages_file.parent.mkdir(parents=True, exist_ok=True)
    saved_messages = [asdict(message) for message in custom_messages]
    custom_messages_file.write_text(
        json.dumps(saved_messages, indent=4),
        encoding="utf-8",
    )


def load_custom_messages() -> list[Fortune]:
    if not custom_messages_file.exists():
        return []

    saved_messages = json.loads(custom_messages_file.read_text(encoding="utf-8"))
    try:
        return [Fortune(**message) for message in saved_messages]
    except TypeError as error:
        raise ValueError(f"{custom_messages_file.name} has the wrong format") from error
