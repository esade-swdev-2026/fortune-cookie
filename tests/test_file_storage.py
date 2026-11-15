from pathlib import Path

import pytest

from fortune_cookie import file_storage


def test_saving_creates_the_data_folder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    new_file = tmp_path / "new_folder" / "last.txt"
    monkeypatch.setattr(file_storage, "last_message_file", new_file)
    file_storage.save_last_message("Hi")
    assert new_file.read_text(encoding="utf-8") == "Hi"
