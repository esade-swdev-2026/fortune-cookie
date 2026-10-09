import typer

from fortune_cookie.core import filter_by_category, get_fortune, lucky_numbers

messages = [
    {"text": "Believe in yourself", "category": "motivation"},
    {"text": "Love is coming", "category": "love"},
    {"text": "Success is near", "category": "career"},
    {"text": "Great opportunities await you", "category": "career"},
    {"text": "Trust your instincts", "category": "motivation"},
]

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
        selected_message = get_fortune(matching_messages)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error

    typer.echo(f"Your fortune for [{category}]: {selected_message['text']}")
    generated_lucky_numbers = lucky_numbers()
    typer.echo(f"Your lucky numbers today are {generated_lucky_numbers}!")


if __name__ == "__main__":
    app()
