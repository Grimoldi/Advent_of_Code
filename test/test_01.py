import pytest

import day_01
from utils import load_input_data


def test_double_digit_number_calculation() -> None:
    """Test that given a list of single digits integers, the double digit number is what's expected."""
    numbers = [1, 2, 3, 4, 5, 6, 7]
    double_digits = day_01.get_digits_from_list(numbers)
    assert double_digits == 17


def test_first_question() -> None:
    """Test the first question."""
    data = load_input_data("01_f_test")
    numbers = day_01.find_double_digit_coordinate(data)
    expected_result = [12, 38, 15, 77]
    assert numbers == expected_result
    assert sum(numbers) == 142


def test_second_question() -> None:
    """Test the second question."""
    data = load_input_data("01_s_test")
    numbers = day_01.find_double_digit_coordinate_even_from_string(data)
    expected_result = [29, 83, 13, 24, 42, 14, 76]
    assert numbers == expected_result
    assert sum(numbers) == 281
