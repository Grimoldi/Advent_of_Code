import pytest

import day_02

EXAMPLE = "02_test"
REAL = "02_input"


def test_first_question(filename=EXAMPLE) -> None:
    """Test the first question with example data."""
    actual = day_02._sum_invalid_ids(filename)
    expected = 1227775554

    assert actual == expected


def test_first_question_real(filename=REAL) -> None:
    """Test the first question."""
    actual = day_02._sum_invalid_ids(filename)
    expected = 12586854255

    assert actual == expected


def test_second_question(filename=EXAMPLE) -> None:
    """Test the second question with example data."""
    actual = day_02._sum_invalid_ids_chunks(filename)
    expected = 4174379265

    assert actual == expected


def test_second_question_real(filename=REAL) -> None:
    """Test the second question with example data."""
    actual = day_02._sum_invalid_ids_chunks(filename)
    expected = 17298174201

    assert actual == expected


test_data = [
    (11, True),
    (99, True),
    (98, False),
    (12, False),
    (101, False),
    (1010, True),
]


@pytest.mark.parametrize("_id, expected", test_data)
def test_id_validation_match(_id, expected) -> None:
    """Test the validation of an id."""
    actual = day_02._invalid_id(_id)

    assert actual == expected


test_data = [
    (11, 22, [11, 22]),
    (95, 115, [99]),
    (998, 1012, [1010]),
    (1698522, 1698528, []),
]


@pytest.mark.parametrize("inf, sup, expected", test_data)
def test_find_invalid_id_in_range(inf, sup, expected) -> None:
    """Test the validation of an id."""
    actual = day_02._find_invalid_ids(inf, sup)

    assert actual == expected


test_data = [
    (11, True),
    (999, True),
    (1010, True),
    (446446, True),
    (12, False),
    (101, False),
]


@pytest.mark.parametrize("_id, expected", test_data)
def test_find_invalid_id_with_chunks(_id, expected) -> None:
    """Test the validation of an id."""
    actual = day_02._invalid_id_chunks(_id)

    assert actual == expected
