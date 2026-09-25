import typer

app = typer.Typer(
    help="Fortune Cookie is a lightweight command-line utility to generate personalized fortunes."
)


@app.callback()
def main() -> None:
    """Fortune Cookie CLI."""


@app.command()
def get(category: str, lucky_number: int = 7) -> None:
    """Generate a fortune for a specific category."""
    if lucky_number < 1:
        typer.echo("lucky number must be at least 1", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Your fortune for [{category}]: Your lucky number today is {lucky_number}!")


if __name__ == "__main__":
    app()
