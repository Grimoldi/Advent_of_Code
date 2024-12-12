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


def test_rules_sorting() -> None:
    rules, _ = day_05._build_data_from(FIRST_EXAMPLE)
    sorted_rules = day_05._sort_rules(rules)

    actual = sorted_rules[0]
    expected = (29, 13)
    assert actual == expected

    actual = sorted_rules[-1]
    expected = (97, 75)
    assert actual == expected


def test_resort_of_pages_for_single_rule() -> None:
    actual = [75, 97, 47, 61, 53]
    rule = (97, 75)
    day_05._resort_by_single(actual, rule)
    expected = [97, 75, 47, 61, 53]

    assert actual == expected


def test_sum_of_reordered_pages() -> None:
    rules, pages = day_05._build_data_from(FIRST_EXAMPLE)
    rules = day_05._sort_rules(rules)
    actual = day_05._calculate_sum_of_incorrect_middlepages(pages, rules)
    expected = 123

    assert actual == expected


def test_several_reorder_of_incorrect_list() -> None:
    rules, batches = day_05._build_data_from(FIRST_EXAMPLE)
    rules = day_05._sort_rules(rules)
    # [97, 13, 75, 29, 47]
    pages = batches[-1]

    for rule in rules:
        is_correct_order = day_05._check_order_of_by_single(pages, rule)
        if is_correct_order:
            continue

        day_05._resort_by_single(pages, rule)

    actual = pages
    expected = [97, 75, 47, 29, 13]
    assert actual == expected
