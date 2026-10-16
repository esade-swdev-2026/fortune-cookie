import json
from dataclasses import asdict
from pathlib import Path

from fortune_cookie.fortune_rules import Fortune

history_file = Path.home() / ".fortune_cookie_history.json"
last_message_file = Path.home() / ".fortune_cookie_last.txt"
custom_messages_file = Path.home() / ".fortune_cookie_messages.json"


def load_history() -> set[str]:
    if not history_file.exists():
        return set()

    with open(history_file, encoding="utf-8") as file:
        saved_messages = json.load(file)

    return set(saved_messages)


def save_history(seen_messages: set[str]) -> None:
    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(sorted(seen_messages), file)


def load_last_message() -> str | None:
    if not last_message_file.exists():
        return None

    return last_message_file.read_text(encoding="utf-8")


def save_last_message(message: str) -> None:
    last_message_file.write_text(message, encoding="utf-8")


def save_custom_messages(custom_messages: list[Fortune]) -> None:
    saved_messages = [asdict(message) for message in custom_messages]
    custom_messages_file.write_text(
        json.dumps(saved_messages, indent=4),
        encoding="utf-8",
    )


def load_custom_messages() -> list[Fortune]:
    if not custom_messages_file.exists():
        return []

    saved_messages = json.loads(custom_messages_file.read_text(encoding="utf-8"))
    return [Fortune(**message) for message in saved_messages]
