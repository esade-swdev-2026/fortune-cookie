from fortune_cookie.fortune_rules import Fortune, list_categories


def test_list_categories_returns_each_category_once_in_order() -> None:
    messages = [
        Fortune(text="Work hard", category="motivation"),
        Fortune(text="Ask for a raise", category="career"),
        Fortune(text="Smile today", category="motivation"),
    ]

    assert list_categories(messages) == ["career", "motivation"]


def test_list_categories_of_an_empty_list_is_empty() -> None:
    assert list_categories([]) == []
