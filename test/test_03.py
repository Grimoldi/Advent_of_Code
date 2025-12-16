import pytest

import day_03

EXAMPLE = "03_test"
REAL = "03_input"


def test_first_question(filename=EXAMPLE) -> None:
    """Test the first question with example data."""
    actual = day_03._sum_bank_joltage(filename)
    expected = 357

    assert actual == expected


def test_first_question_real(filename=REAL) -> None:
    """Test the first question."""
    actual = day_03._sum_bank_joltage(filename)
    expected = 17376

    assert actual == expected


def test_second_question(filename=EXAMPLE) -> None:
    """Test the second question with example data."""


def test_second_question_real(filename=REAL) -> None:
    """Test the second question with example data."""


test_data = [
    (987654321111111, 98),
    (811111111111119, 89),
    (234234234234278, 78),
    (818181911112111, 92),
]


@pytest.mark.parametrize("batteries, expected", test_data)
def test_find_bank_joltage(batteries, expected) -> None:
    """Test the joltage from a bank."""
    actual = day_03._find_bank_joltage([int(x) for x in str(batteries)])

    assert actual == expected
