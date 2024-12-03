from typing import TYPE_CHECKING

import day_03  # type: ignore

if TYPE_CHECKING:
    from src import day_03

FIRST_EXAMPLE = "03_first_example"
SECOND_EXAMPLE = "03_second_example"


def test_load_data() -> None:
    actual = day_03._build_data_from(FIRST_EXAMPLE)
    expected = ["mul(2,4)", "mul(5,5)", "mul(11,8)", "mul(8,5)"]
    assert expected == actual


def test_multiply_from_string() -> None:
    actual = day_03._multiply_couple("mul(2,4)")
    expected = 8
    assert expected == actual


def test_calculate_total() -> None:
    actual = day_03._calculate_total_sum_from(FIRST_EXAMPLE)
    expected = 161
    assert expected == actual


def test_enabled_instructions() -> None:
    actual = day_03._build_enabled_data_from(SECOND_EXAMPLE)
    expected = ["mul(2,4)", "mul(8,5)"]
    assert expected == actual


def test_calculate_total_of_enabled() -> None:
    actual = day_03._calculate_total_sum_of_enabled_instructions_from(SECOND_EXAMPLE)
    expected = 48
    assert expected == actual
