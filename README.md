# fortune-cookie

Fortune Cookie is a command-line utility for students and terminal users who want to instantly generate random fortunes and lucky numbers.

## Install

```
uv sync
```

This creates a virtual environment and installs everything, including the development
tools, from `uv.lock` — the committed file that pins exact versions so every teammate
and CI resolve the same ones. When you change a dependency in `pyproject.toml`, run
`uv lock` and commit the updated `uv.lock`; CI fails if the two disagree.

## Run

```
uv run fortune-cookie get career --lucky-number 5
uv run fortune-cookie count
uv run fortune-cookie many 3
uv run fortune-cookie add "Smile today" motivation
uv run fortune-cookie last
```

`--lucky-number` sets how many lucky numbers are printed (1 to 49, default 6).

Data is saved in your home folder: `~/.fortune_cookie_history.json` (fortunes already shown), `~/.fortune_cookie_last.txt` (the last fortune) and `~/.fortune_cookie_messages.json` (fortunes you add).

## Develop

```
uv run ruff check .          # lint
uv run ruff format .         # format (CI runs `--check` and fails on a diff)
uv run mypy src tests        # types
uv run pytest                # tests
```

These four commands are exactly what `.github/workflows/check.yml` runs on every push.
If they pass here, CI passes.

## Layout

```
src/fortune_cookie/   the application package
  fortune_rules.py    the pure logic: no files, no printing
  file_storage.py     all file I/O: load_* and save_* for history, last and custom fortunes
  cli.py              the typer command-line interface
  __main__.py         lets `python -m fortune_cookie` work
tests/                pytest tests, mirroring src/
pyproject.toml        dependencies and tool configuration
```

## I/O (shell)
All file I/O lives in `src/fortune_cookie/file_storage.py`. The `cli.py` module handles the Typer command-line interface, including `typer.echo` and `raise typer.Exit`, and calls the `load_*` and `save_*` functions from `file_storage.py` to read and write the history, last fortune, and custom fortunes files. No I/O anywhere else.

## Commands

| Command | What it does |
|---|---|
| `get <category>` | Shows a random fortune from that category, with your lucky numbers. `--lucky-number N` chooses how many numbers (1 to 49, default 6). |
| `count` | Shows how many fortunes there are in total. |
| `many <n>` | Shows `n` random fortunes at once, including the ones you added. |
| `add "<text>" <category>` | Saves your own fortune in that category, so it can come up later. |
| `last` | Shows the last fortune you got, or tells you none has been shown yet. |
