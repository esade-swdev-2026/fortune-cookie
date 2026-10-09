import json
from dataclasses import asdict
from pathlib import Path

import typer

from fortune_cookie.core import (
    Fortune,
    add_message,
    count_messages,
    filter_by_category,
    get_fresh_fortune,
    get_many,
    lucky_numbers,
)

history_file = Path.home() / ".fortune_cookie_history.json"

messages = [
    Fortune(text="Believe in yourself", category="motivation"),
    Fortune(text="Love is coming", category="love"),
    Fortune(text="Success is near", category="career"),
    Fortune(text="Great opportunities await you", category="career"),
    Fortune(text="Trust your instincts", category="motivation"),
]

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
        all_messages = messages + load_custom_messages()
        matching_messages = filter_by_category(all_messages, category)
        seen_messages = load_history()

        if all(message.text in seen_messages for message in matching_messages):
            last_message = (
                last_message_file.read_text(encoding="utf-8")
                if last_message_file.exists()
                else None
            )

            seen_messages.difference_update(message.text for message in matching_messages)

            if last_message is not None and any(
                message.text != last_message for message in matching_messages
            ):
                seen_messages.add(last_message)

        selected_message = get_fresh_fortune(matching_messages, seen_messages)
        save_history(seen_messages)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error

    typer.echo(f"Your fortune for [{category}]: {selected_message.text}")
    save_last_message(selected_message.text)
    generated_lucky_numbers = lucky_numbers()
    typer.echo(f"Your lucky numbers today are {generated_lucky_numbers}!")


@app.command()
def count() -> None:
    all_messages = messages + load_custom_messages()
    total_messages = count_messages(all_messages)
    typer.echo(f"Total fortunes: {total_messages}")


@app.command()
def many(number_of_messages: int) -> None:
    try:
        all_messages = messages + load_custom_messages()
        selected_messages = get_many(all_messages, number_of_messages)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error

    for message in selected_messages:
        typer.echo(message.text)


@app.command()
def add(text: str, category: str) -> None:
    try:
        custom_messages = load_custom_messages()
        updated_messages = add_message(custom_messages, text, category)
        save_custom_messages(updated_messages)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error

    typer.echo(f"Fortune added: {text}")


@app.command()
def last() -> None:
    if not last_message_file.exists():
        typer.echo("No fortune has been displayed yet.")
        return

    last_message = last_message_file.read_text(encoding="utf-8")
    typer.echo(f"Your last fortune: {last_message}")


if __name__ == "__main__":
    app()
