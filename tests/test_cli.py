import re
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


def test_get_fortune_prints_the_requested_amount_of_lucky_numbers() -> None:
    result = runner.invoke(app, ["get", "career", "--lucky-number", "3"])
    assert result.exit_code == 0
    lucky_numbers_found = re.findall(r"\d+", result.stdout.splitlines()[-1])
    assert len(lucky_numbers_found) == 3


def test_get_fortune_rejects_more_than_49_lucky_numbers() -> None:
    result = runner.invoke(app, ["get", "career", "--lucky-number", "50"])
    assert result.exit_code == 1


def test_categories_lists_each_category_once_in_order() -> None:
    result = runner.invoke(app, ["categories"])
    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["career", "love", "motivation"]


def test_categories_includes_categories_from_added_fortunes() -> None:
    add_result = runner.invoke(app, ["add", "A journey begins", "travel"])
    assert add_result.exit_code == 0
    result = runner.invoke(app, ["categories"])
    assert result.exit_code == 0
    assert "travel" in result.stdout.splitlines()


def test_categories_fails_on_corrupted_json(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_load_custom_messages() -> list[dict[str, str]]:
        raise ValueError("Invalid JSON format")

    monkeypatch.setattr("fortune_cookie.cli.load_custom_messages", mock_load_custom_messages)

    result = runner.invoke(app, ["categories"])
    assert result.exit_code == 1
    assert "Could not load categories: Invalid JSON format" in result.output


def test_add_rejects_a_fortune_that_is_already_built_in() -> None:
    result = runner.invoke(app, ["add", "Believe in yourself", "motivation"])
    assert result.exit_code == 1
    assert "already exists" in result.output


def test_add_shows_the_cleaned_text() -> None:
    result = runner.invoke(app, ["add", "  Smile today  ", "motivation"])
    assert result.exit_code == 0
    assert "Fortune added: Smile today\n" in result.output


def test_count_shows_the_built_in_fortunes() -> None:
    result = runner.invoke(app, ["count"])
    assert result.exit_code == 0
    assert result.stdout == "Total fortunes: 5\n"


def test_count_includes_added_fortunes() -> None:
    runner.invoke(app, ["add", "Smile today", "motivation"])
    result = runner.invoke(app, ["count"])
    assert result.stdout == "Total fortunes: 6\n"


def test_count_fails_cleanly_on_a_corrupted_messages_file() -> None:
    file_storage.custom_messages_file.write_text("{bad", encoding="utf-8")
    result = runner.invoke(app, ["count"])
    assert result.exit_code == 1
    assert "Could not load fortunes" in result.output
    assert "Traceback" not in result.output


def test_many_prints_the_requested_number_of_fortunes() -> None:
    result = runner.invoke(app, ["many", "3"])
    assert result.exit_code == 0
    assert len(result.stdout.splitlines()) == 3


@pytest.mark.parametrize("amount", ["0", "6"])
def test_many_rejects_an_amount_outside_the_available_range(amount: str) -> None:
    result = runner.invoke(app, ["many", amount])
    assert result.exit_code == 1
    assert "between 1 and the total available" in result.output


def test_last_says_so_when_no_fortune_was_shown_yet() -> None:
    result = runner.invoke(app, ["last"])
    assert result.exit_code == 0
    assert "No fortune has been displayed yet." in result.output


def test_last_shows_the_fortune_that_get_displayed() -> None:
    get_result = runner.invoke(app, ["get", "love"])
    assert get_result.exit_code == 0
    result = runner.invoke(app, ["last"])
    assert "Your last fortune: Love is coming" in result.output


def test_get_with_an_unknown_category_fails_with_a_message() -> None:
    result = runner.invoke(app, ["get", "health"])
    assert result.exit_code == 1
    assert "Category 'health' does not exist" in result.output


def test_count_fails_cleanly_on_a_messages_file_with_the_wrong_shape() -> None:
    file_storage.custom_messages_file.write_text('[{"message": "hi"}]', encoding="utf-8")
    result = runner.invoke(app, ["count"])
    assert result.exit_code == 1
    assert "Could not load fortunes" in result.output
    assert "Traceback" not in result.output
