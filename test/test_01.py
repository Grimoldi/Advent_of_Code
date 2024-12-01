from typing import TYPE_CHECKING

import pytest

import day_01  # type: ignore

if TYPE_CHECKING:
    from src import day_01

FIRST_EXAMPLE = "01_first_example"


def test_load_data() -> None:
    numbers = day_01._build_data(FIRST_EXAMPLE)
    expected_result = ([1, 2, 3, 3, 3, 4], [3, 3, 3, 4, 5, 9])
    assert numbers == expected_result


def test_first_question() -> None:
    """Test the first question."""
    total_distance = day_01._find_total_distance(FIRST_EXAMPLE)
    assert total_distance == 11


@pytest.mark.skip()
def test_second_question() -> None:
    """Test the second question."""
    data = load_input_data("01_first_example")
    numbers = day_01.find_double_digit_coordinate_even_from_string(data)
    expected_result = [29, 83, 13, 24, 42, 14, 76]
    assert numbers == expected_result
    assert sum(numbers) == 281
    assert numbers == expected_result
    assert sum(numbers) == 281
    assert numbers == expected_result
    assert sum(numbers) == 281
