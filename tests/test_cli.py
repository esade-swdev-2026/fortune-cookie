from typer.testing import CliRunner

from fortune_cookie.cli import app

runner = CliRunner()


def test_get_fortune_success() -> None:
    result = runner.invoke(app, ["get", "career", "--lucky-number", "5"])
    assert result.exit_code == 0
    assert "career" in result.stdout


def test_get_fortune_invalid_number() -> None:
    result = runner.invoke(app, ["get", "career", "--lucky-number", "0"])
    assert result.exit_code == 1
