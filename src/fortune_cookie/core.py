import random


def get_fortune(messages: list[dict[str, str]]) -> dict[str, str]:
    if not messages:
        raise ValueError("Cannot choose a fortune from an empty list")

    return random.choice(messages)


def count_messages(messages: list[dict[str, str]]) -> int:
    return len(messages)


def get_fresh_fortune(messages: list[dict[str, str]], seen: set[str]) -> dict[str, str]:
    if not messages:
        raise ValueError("Cannot choose a fortune from an empty list")

    available_messages = [message for message in messages if message["text"] not in seen]

    if not available_messages:
        seen.clear()
        available_messages = messages

    selected_message = random.choice(available_messages)
    seen.add(selected_message["text"])

    return selected_message


def lucky_numbers(number_of_lucky_numbers: int = 6) -> list[int]:
    if number_of_lucky_numbers < 1 or number_of_lucky_numbers > 49:
        raise ValueError("Number of lucky numbers must be between 1 and 49")

    return random.sample(range(1, 50), number_of_lucky_numbers)


def filter_by_category(messages: list[dict[str, str]], category: str) -> list[dict[str, str]]:
    available_categories = {message["category"] for message in messages}

    if category not in available_categories:
        raise ValueError(f"Category '{category}' does not exist")

    matching_messages = [message for message in messages if message["category"] == category]

    return matching_messages


def add_message(messages: list[dict[str, str]], text: str, category: str) -> list[dict[str, str]]:
    if not text.strip():
        raise ValueError("Message cannot be empty")

    if not category.strip():
        raise ValueError("Category cannot be empty")

    new_message = {"text": text.strip(), "category": category.strip()}

    return messages + [new_message]


def get_many(messages: list[dict[str, str]], number_of_messages: int) -> list[dict[str, str]]:
    if number_of_messages < 1 or number_of_messages > len(messages):
        raise ValueError("Number of messages must be between 1 and the total available")

    return random.sample(messages, number_of_messages)
