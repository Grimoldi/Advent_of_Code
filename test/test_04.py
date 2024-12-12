from typing import TYPE_CHECKING

import day_04  # type: ignore

if TYPE_CHECKING:
    from src import day_04

FIRST_EXAMPLE = "04_first_example"
XMAS = ["X", "M", "A", "S"]


def test_load() -> None:
    data = day_04._build_data_from(FIRST_EXAMPLE)
    actual = data[0]
    expected = ["M", "M", "M", "S", "X", "X", "M", "A", "S", "M"]

    assert expected == actual


def test_extract_row() -> None:
    line = ["M", "S", "A", "M", "X", "M", "S", "M", "S", "A"]
    actual = day_04._extract_row_from(line)
    expected = [
        ["M", "S", "A", "M"],
        ["S", "A", "M", "X"],
        ["A", "M", "X", "M"],
        ["M", "X", "M", "S"],
        ["X", "M", "S", "M"],
        ["M", "S", "M", "S"],
        ["S", "M", "S", "A"],
    ]

    assert expected == actual


def test_check_xmas() -> None:
    actual = day_04._check_for_xmas_from(XMAS)
    assert actual is True


def test_check_reverse_xmas() -> None:
    actual = day_04._check_for_xmas_from(XMAS[::-1])
    assert actual is True


def test_check_no_xmas() -> None:
    wrong_xmas = ["M", "M", "A", "S"]
    actual = day_04._check_for_xmas_from(wrong_xmas)
    assert actual is False


def test_horizontal_search() -> None:
    data = day_04._build_data_from(FIRST_EXAMPLE)
    partial_data = data[0:2]
    actual = len(day_04._extract_horizontal_batch_from(partial_data))
    # the columns lesser 3 (last three positions can't be a 4 letter lenght) times 2 lines
    expected = (len(data) - 3) * 2

    assert expected == actual


def test_vertial_search() -> None:
    data = day_04._build_data_from(FIRST_EXAMPLE)
    partial_data = data[0:5]
    actual = len(day_04._extract_vertical_batch_from(partial_data))
    # the columns times 2 (in 5 position we have 2 words 4 letters long)
    expected = len(data) * 2

    assert expected == actual


def test_diagonal_left_right_search() -> None:
    partial_data = [
        ["M", "S", "A", "M", "S"],
        ["S", "A", "M", "X", "A"],
        ["A", "M", "X", "M", "X"],
        ["M", "X", "M", "S", "M"],
        ["X", "M", "S", "M", "X"],
    ]
    actual = len(day_04._extract_diagonally_from_left_to_right_from(partial_data))
    # from 0,0 to 3,3
    # from 0,1 to 3,4
    # from 1,0 to 4,3
    # from 1,1 to 4,4
    expected = 4

    assert expected == actual


def test_mirror_report() -> None:
    partial_data = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]
    expected = [
        ["3", "2", "1"],
        ["6", "5", "4"],
        ["9", "8", "7"],
    ]
    actual = day_04._revert(partial_data)

    assert actual == expected


def test_extract_right_to_left() -> None:
    partial_data = [
        ["1", "2", "3", "4"],
        ["5", "6", "7", "8"],
        ["9", "10", "11", "12"],
        ["13", "14", "15", "16"],
    ]
    expected = [["4", "7", "10", "13"]]
    actual = day_04._extract_diagonally_from_right_to_left_from(partial_data, 4)

    assert expected == actual


def test_first_question() -> None:
    actual = day_04._count_xmas_from(FIRST_EXAMPLE)
    expected = 18

    assert expected == actual
