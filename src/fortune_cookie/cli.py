from typing import Annotated

import typer

from fortune_cookie.file_storage import (
    load_custom_messages,
    load_history,
    load_last_message,
    save_custom_messages,
    save_history,
    save_last_message,
)
from fortune_cookie.fortune_rules import (
    DEFAULT_LUCKY_NUMBER_COUNT,
    Fortune,
    add_message,
    count_messages,
    filter_by_category,
    get_fresh_fortune,
    get_many,
    lucky_numbers,
    reset_when_all_seen,
)

messages = [
    Fortune(text="Believe in yourself", category="motivation"),
    Fortune(text="Love is coming", category="love"),
    Fortune(text="Success is near", category="career"),
    Fortune(text="Great opportunities await you", category="career"),
    Fortune(text="Trust your instincts", category="motivation"),
]


app = typer.Typer(
    help="Fortune Cookie is a lightweight command-line utility to generate personalized fortunes."
)


@app.callback()
def main() -> None:
    pass


@app.command()
def get(
    category: str,
    lucky_count: Annotated[int, typer.Option("--lucky-number")] = DEFAULT_LUCKY_NUMBER_COUNT,
) -> None:
    try:
        all_messages = messages + load_custom_messages()
        matching_messages = filter_by_category(all_messages, category)
        seen_messages = reset_when_all_seen(matching_messages, load_history(), load_last_message())
        selected_message = get_fresh_fortune(matching_messages, seen_messages)
        generated_lucky_numbers = lucky_numbers(lucky_count)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error

    save_history(seen_messages | {selected_message.text})
    save_last_message(selected_message.text)
    typer.echo(f"Your fortune for [{category}]: {selected_message.text}")
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
    last_message = load_last_message()

    if last_message is None:
        typer.echo("No fortune has been displayed yet.")
        return

    typer.echo(f"Your last fortune: {last_message}")


if __name__ == "__main__":
    app()
