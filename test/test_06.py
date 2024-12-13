from typing import TYPE_CHECKING

import pytest
from ordered_set import OrderedSet

import day_06  # type: ignore

if TYPE_CHECKING:
    from src import day_06

FIRST_EXAMPLE = "06_first_example"


def test_find_the_guard() -> None:
    _map = day_06._build_data_from(FIRST_EXAMPLE)
    actual = day_06._find_the_guard(_map)
    expected = (4, 6)

    assert actual == expected


def test_get_free_cell() -> None:
    _map = day_06._build_data_from(FIRST_EXAMPLE)
    actual = day_06._get_cell_from(_map, 2, 0)
    expected = day_06.FREE

    assert actual == expected


def test_get_blocked_cell() -> None:
    _map = day_06._build_data_from(FIRST_EXAMPLE)
    actual = day_06._get_cell_from(_map, 4, 0)
    expected = day_06.BLOCKED

    assert actual == expected


def test_get_outer_cell() -> None:
    _map = day_06._build_data_from(FIRST_EXAMPLE)
    with pytest.raises(IndexError):
        day_06._get_cell_from(_map, len(_map) + 1, 4)


def test_steps_made() -> None:
    _map = day_06._build_data_from(FIRST_EXAMPLE)
    x, y = day_06._find_the_guard(_map)
    visited = OrderedSet({})
    guard = day_06.Guard(x, y, visited)

    actual = day_06._count_the_visited_cells(guard, _map)
    expected = 41
    print(guard.visited_cell)
    assert actual == expected
