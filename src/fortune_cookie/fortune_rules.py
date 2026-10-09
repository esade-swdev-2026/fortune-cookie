import random
from dataclasses import dataclass

LOWEST_LUCKY_NUMBER = 1
HIGHEST_LUCKY_NUMBER = 49
DEFAULT_LUCKY_NUMBER_COUNT = 6


@dataclass(frozen=True)
class Fortune:
    text: str
    category: str


def get_fortune(messages: list[Fortune]) -> Fortune:
    if not messages:
        raise ValueError("Cannot choose a fortune from an empty list")
    return random.choice(messages)


def count_messages(messages: list[Fortune]) -> int:
    return len(messages)


def get_fresh_fortune(messages: list[Fortune], seen: set[str]) -> Fortune:
    if not messages:
        raise ValueError("Cannot choose a fortune from an empty list")

    available_messages = [message for message in messages if message.text not in seen]

    if not available_messages:
        raise ValueError("No unseen fortunes available")

    return random.choice(available_messages)


def reset_when_all_seen(
    messages: list[Fortune], seen: set[str], last_message: str | None
) -> set[str]:
    if not all(message.text in seen for message in messages):
        return set(seen)

    remaining = seen - {message.text for message in messages}

    if last_message is not None and any(message.text != last_message for message in messages):
        remaining.add(last_message)

    return remaining


def lucky_numbers(number_of_lucky_numbers: int = DEFAULT_LUCKY_NUMBER_COUNT) -> list[int]:
    if not LOWEST_LUCKY_NUMBER <= number_of_lucky_numbers <= HIGHEST_LUCKY_NUMBER:
        raise ValueError(
            f"Number of lucky numbers must be between {LOWEST_LUCKY_NUMBER} "
            f"and {HIGHEST_LUCKY_NUMBER}"
        )

    return random.sample(
        range(LOWEST_LUCKY_NUMBER, HIGHEST_LUCKY_NUMBER + 1), number_of_lucky_numbers
    )


def filter_by_category(messages: list[Fortune], category: str) -> list[Fortune]:
    available_categories = {message.category for message in messages}

    if category not in available_categories:
        raise ValueError(f"Category '{category}' does not exist")

    matching_messages = [message for message in messages if message.category == category]
    return matching_messages


def add_message(messages: list[Fortune], text: str, category: str) -> list[Fortune]:
    if not text.strip():
        raise ValueError("Message cannot be empty")

    if not category.strip():
        raise ValueError("Category cannot be empty")

    new_message = Fortune(text=text.strip(), category=category.strip())
    return messages + [new_message]


def get_many(messages: list[Fortune], number_of_messages: int) -> list[Fortune]:
    if number_of_messages < 1 or number_of_messages > len(messages):
        raise ValueError("Number of messages must be between 1 and the total available")

    return random.sample(messages, number_of_messages)
