from pathlib import Path

import pytest
from typer.testing import CliRunner

from fortune_cookie import file_storage
from fortune_cookie.cli import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def files_in_tmp_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(file_storage, "history_file", tmp_path / "history.json")
    monkeypatch.setattr(file_storage, "last_message_file", tmp_path / "last.txt")
    monkeypatch.setattr(file_storage, "custom_messages_file", tmp_path / "messages.json")


def test_get_fortune_success() -> None:
    result = runner.invoke(app, ["get", "career", "--lucky-number", "5"])
    assert result.exit_code == 0
    assert "career" in result.stdout


def test_get_fortune_invalid_number() -> None:
    result = runner.invoke(app, ["get", "career", "--lucky-number", "0"])
    assert result.exit_code == 1
