import pytest

from fortune_cookie.core import (
    Fortune,
    add_message,
    count_messages,
    filter_by_category,
    get_fortune,
    get_fresh_fortune,
    get_many,
    lucky_numbers,
)

LOVE = Fortune(text="Love is coming", category="love")
CAREER = Fortune(text="Success is near", category="career")
CAREER_2 = Fortune(text="Great opportunities await you", category="career")


@pytest.fixture
def messages() -> list[Fortune]:
    return [LOVE, CAREER, CAREER_2]


def test_count_messages_returns_number_of_fortunes(messages: list[Fortune]) -> None:
    assert count_messages(messages) == 3


def test_count_of_empty_list_is_zero() -> None:
    assert count_messages([]) == 0


def test_get_fortune_returns_one_of_the_messages(messages: list[Fortune]) -> None:
    assert get_fortune(messages) in messages


def test_get_fortune_from_empty_list_raises() -> None:
    with pytest.raises(ValueError):
        get_fortune([])


def test_filter_keeps_only_the_chosen_category(messages: list[Fortune]) -> None:
    assert filter_by_category(messages, "career") == [CAREER, CAREER_2]


def test_filter_unknown_category_raises(messages: list[Fortune]) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        filter_by_category(messages, "health")


def test_fresh_fortune_skips_seen_messages(messages: list[Fortune]) -> None:
    seen = {LOVE.text, CAREER.text}
    assert get_fresh_fortune(messages, seen) == CAREER_2


def test_fresh_fortune_is_added_to_seen(messages: list[Fortune]) -> None:
    seen: set[str] = set()
    chosen = get_fresh_fortune(messages, seen)
    assert seen == {chosen.text}


def test_fresh_fortune_raises_when_everything_was_seen(messages: list[Fortune]) -> None:
    seen = {message.text for message in messages}
    with pytest.raises(ValueError, match="No unseen"):
        get_fresh_fortune(messages, seen)


def test_lucky_numbers_default_is_six_unique_numbers_between_1_and_49() -> None:
    numbers = lucky_numbers()
    assert len(numbers) == 6
    assert len(set(numbers)) == 6
    assert all(1 <= number <= 49 for number in numbers)


@pytest.mark.parametrize("amount", [1, 49])
def test_lucky_numbers_accepts_the_boundaries(amount: int) -> None:
    assert len(lucky_numbers(amount)) == amount


@pytest.mark.parametrize("amount", [0, 50, -1])
def test_lucky_numbers_outside_1_to_49_raises(amount: int) -> None:
    with pytest.raises(ValueError):
        lucky_numbers(amount)


def test_add_message_appends_a_cleaned_fortune(messages: list[Fortune]) -> None:
    result = add_message(messages, "  Smile today  ", " motivation ")
    assert result[-1] == Fortune(text="Smile today", category="motivation")
    assert len(result) == 4


def test_add_message_does_not_change_the_original_list(messages: list[Fortune]) -> None:
    add_message(messages, "Smile today", "motivation")
    assert len(messages) == 3


@pytest.mark.parametrize(("text", "category"), [("", "love"), ("   ", "love"), ("Hi", "  ")])
def test_add_message_with_blank_text_or_category_raises(text: str, category: str) -> None:
    with pytest.raises(ValueError):
        add_message([], text, category)


def test_get_many_returns_that_many_different_messages(messages: list[Fortune]) -> None:
    result = get_many(messages, 2)
    assert len(result) == 2
    assert len(set(result)) == 2
    assert all(message in messages for message in result)


@pytest.mark.parametrize("amount", [0, 4])
def test_get_many_outside_the_available_range_raises(messages: list[Fortune], amount: int) -> None:
    with pytest.raises(ValueError):
        get_many(messages, amount)
