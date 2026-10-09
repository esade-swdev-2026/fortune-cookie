import json
from pathlib import Path

import typer

from fortune_cookie.core import filter_by_category, get_fresh_fortune, lucky_numbers

history_file = Path.home() / ".fortune_cookie_history.json"

messages = [
    {"text": "Believe in yourself", "category": "motivation"},
    {"text": "Love is coming", "category": "love"},
    {"text": "Success is near", "category": "career"},
    {"text": "Great opportunities await you", "category": "career"},
    {"text": "Trust your instincts", "category": "motivation"},
]

last_message_file = Path.home() / ".fortune_cookie_last.txt"

def load_history() -> set[str]:
    if not history_file.exists():
        return set()

    with open(history_file, encoding="utf-8") as file:
        saved_messages = json.load(file)

    return set(saved_messages)


def save_history(seen_messages: set[str]) -> None:
    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(sorted(seen_messages), file)

def save_last_message(message: str) -> None:
    last_message_file.write_text(message, encoding="utf-8")

app = typer.Typer(
    help="Fortune Cookie is a lightweight command-line utility to generate personalized fortunes."
)


@app.callback()
def main() -> None:
    """Fortune Cookie CLI."""


@app.command()
def get(category: str, lucky_number: int = 7) -> None:
    if lucky_number < 1:
        typer.echo("Lucky number must be at least 1", err=True)
        raise typer.Exit(code=1)
    try:
        matching_messages = filter_by_category(messages, category)
        seen_messages = load_history()

        if all(message["text"] in seen_messages for message in matching_messages):
            seen_messages.difference_update(message["text"] for message in matching_messages)

        selected_message = get_fresh_fortune(matching_messages, seen_messages)
        save_history(seen_messages)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error

    typer.echo(f"Your fortune for [{category}]: {selected_message['text']}")
    save_last_message(selected_message["text"])
    generated_lucky_numbers = lucky_numbers()
    typer.echo(f"Your lucky numbers today are {generated_lucky_numbers}!")

@app.command()
def last() -> None:
    if not last_message_file.exists():
        typer.echo("No fortune has been displayed yet.")
        return

    last_message = last_message_file.read_text(encoding="utf-8")
    typer.echo(f"Your last fortune: {last_message}")

if __name__ == "__main__":
    app()
