from typing import TYPE_CHECKING

import day_02  # type: ignore

if TYPE_CHECKING:
    from src import day_02

FIRST_EXAMPLE = "02_first_example"


def test_load_data() -> None:
    reports = day_02._build_data(FIRST_EXAMPLE)
    expected_report = [1, 2, 7, 8, 9]
    assert expected_report == reports[1]


def test_correct_order_increasing() -> None:
    """Test the correct order of a repo."""
    reports = day_02._build_data(FIRST_EXAMPLE)
    actual = day_02._correct_order_of(reports[5])
    assert actual is True


def test_correct_order_decreasing() -> None:
    """Test the correct order of a repo."""
    reports = day_02._build_data(FIRST_EXAMPLE)
    actual = day_02._correct_order_of(reports[0])
    assert actual is True


def test_incorrect_order() -> None:
    """Test the correct order of a repo."""
    reports = day_02._build_data(FIRST_EXAMPLE)
    actual = day_02._correct_order_of(reports[3])
    assert actual is False


def test_correct_order_with_duplicates() -> None:
    """Test the correct order of a repo."""
    reports = day_02._build_data(FIRST_EXAMPLE)
    actual = day_02._correct_order_of(reports[4])
    assert actual is False


def test_first_question() -> None:
    """Test the first question."""
    reports = day_02._build_data(FIRST_EXAMPLE)
    actual = day_02._find_how_many_correct(reports)
    assert actual == 2


def test_second_question() -> None:
    """Test the second question."""
    reports = day_02._build_data(FIRST_EXAMPLE)
    actual = day_02._find_how_many_correct_with_dampener(reports)
    assert actual == 4


def test_second_question_with_random_samples() -> None:
    """Test the second question with random samples."""
    reports = [
        # wrong
        [1, 3, 3, 3, 4],
        [1, 3, 5, 4, 3],
        [46, 50, 51, 52, 59, 60, 61, 60],
        [1, 5, 7, 12, 12],
        [6, 2, 1, 4, 1],
        # correct
        [3, 7, 8, 9],
        [7, 5, 3, 2, 1, 3],
        [7, 5, 3, 2, 1, 3, 0],
        [57, 15, 16, 17, 18, 19],
    ]
    actual = day_02._find_how_many_correct_with_dampener(reports)
    assert actual == 4
