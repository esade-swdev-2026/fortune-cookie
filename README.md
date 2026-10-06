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
```

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
src/app/          your package — importable, installable, not just a script
  cli.py          the typer command-line interface
  __main__.py     lets `python -m fortune_cookie` work
tests/            pytest tests, mirroring src/
pyproject.toml    dependencies and tool configuration — the single source of truth
```

## I/O (shell)
All I/O lives in `src/fortune_cookie/cli.py`: `typer.echo` and `raise typer.Exit` in the CLI command. No file reads/writes, `print` or `sys.exit` anywhere else.
