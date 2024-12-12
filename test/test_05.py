from typing import TYPE_CHECKING

import pytest

import day_05  # type: ignore

if TYPE_CHECKING:
    from src import day_05

FIRST_EXAMPLE = "05_first_example"


def test_rules_load() -> None:
    rules, _ = day_05._build_data_from(FIRST_EXAMPLE)
    actual = rules[0]
    expected = (47, 53)

    assert expected == actual


def test_pages_load() -> None:
    _, pages = day_05._build_data_from(FIRST_EXAMPLE)
    actual = pages[0]
    expected = [75, 47, 61, 53, 29]

    assert expected == actual


def test_check_order_correct() -> None:
    rules, pages = day_05._build_data_from(FIRST_EXAMPLE)
    actual = day_05._check_order_of_by(pages[0], rules)

    assert actual is True


def test_check_order_incorrect() -> None:
    rules, pages = day_05._build_data_from(FIRST_EXAMPLE)
    actual = day_05._check_order_of_by(pages[3], rules)

    assert actual is False


def test_middle_page() -> None:
    data = [1, 2, 3, 4, 5]
    actual = day_05._find_middle_page(data)
    expected = 3

    assert actual == expected


def test_middle_page_error() -> None:
    data = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        day_05._find_middle_page(data)


def test_sum_of_correct_pages() -> None:
    rules, pages = day_05._build_data_from(FIRST_EXAMPLE)
    actual = day_05._calculate_sum_of_middlepages(pages, rules)
    expected = 143

    assert actual == expected
