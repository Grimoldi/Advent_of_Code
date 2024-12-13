import os
from dataclasses import dataclass
from enum import StrEnum, auto

from ordered_set import OrderedSet

import utils

DAY = os.path.basename(__file__).split(".")[0]
FILENAME = "06_first"
logger = utils.setup_logger(utils.create_log_level(False))

FREE = "."
BLOCKED = "#"
GUARD = "^"
Map = list[str]


class Direction(StrEnum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


@dataclass
class Guard:
    x: int
    y: int
    visited_cell: OrderedSet[tuple[int, int]]
    direction: Direction = Direction.UP
    steps: int = 0

    def __post_init__(self) -> None:
        self._mark_cell_as_visited()  # first cell is always visited

    def move_forward(self) -> None:
        """
        Move the guard one step depending on the direction.
        Store the step made.
        """
        logger.info(
            f"Currently in ({self.x},{self.y}), moving forward with direction {self.direction}."
        )
        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.LEFT:
            self.x -= 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        else:
            self.x += 1
        logger.info(f"Now in ({self.x}, {self.y}).")

        self.steps += 1
        self._mark_cell_as_visited()

    def _mark_cell_as_visited(self) -> None:
        """Add to the visited cell the current cell."""
        self.visited_cell.add((self.x, self.y))

    @property
    def distinct_cell_visited(self) -> int:
        """Return how many cell has visited."""
        return len(self.visited_cell)

    def turn_right(self) -> None:
        """Turn the guard right 90 degree."""
        logger.info(f"Turning right from {self.direction}")
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        else:
            self.direction = Direction.DOWN

        logger.info(f"Now pointed to {self.direction}")

    def whats_forward(self) -> tuple[int, int]:
        """Returns the position of the forward cell."""
        if self.direction == Direction.UP:
            return self.x, self.y - 1
        elif self.direction == Direction.LEFT:
            return self.x - 1, self.y
        elif self.direction == Direction.DOWN:
            return self.x, self.y + 1
        else:
            return self.x + 1, self.y

    def whats_on_the_right(self) -> tuple[int, int]:
        """Returns the position of the right cell."""
        if self.direction == Direction.UP:
            return self.x + 1, self.y
        elif self.direction == Direction.LEFT:
            return self.x, self.y + 1
        elif self.direction == Direction.DOWN:
            return self.x - 1, self.y
        else:
            return self.x, self.y - 1


def first_question() -> None:
    """Function to solve the first question."""
    _map = _build_data_from(FILENAME)
    x, y = _find_the_guard(_map)
    visited = OrderedSet({})
    guard = Guard(x, y, visited)
    print(f"First question answer. {_count_the_visited_cells(guard, _map)}")


def second_question() -> None:
    """Function to solve the second question."""
    _ = _build_data_from(FILENAME)
    print("Second question answer. ")


def main() -> None:
    first_question()
    second_question()


def _build_data_from(filename: str) -> Map:
    """Read from the input file the map."""
    return utils.load_input_data(filename)


def _find_the_guard(map: Map) -> tuple[int, int]:
    """Find the guard on the map."""
    for col, line in enumerate(map):
        if GUARD not in line:
            continue

        row = list(line).index(GUARD)
        break

    return row, col


def _get_cell_from(map: Map, x: int, y: int) -> str:
    """Get the cell for a given position."""
    return list(map[y])[x]


def _move_the(guard: Guard, map: Map) -> None:
    """
    Move the guard:
     - forward if free
     - turn right if cannot proceed further
     - exit the map if unable to move forward or turn right
    """
    forward_cell = guard.whats_forward()
    forward_free = _get_cell_from(map, *forward_cell) == FREE
    right_cell = guard.whats_on_the_right()
    right_free = _get_cell_from(map, *right_cell) == FREE

    while forward_free or right_free:
        if forward_free:
            guard.move_forward()
        else:
            guard.turn_right()
        forward_cell = guard.whats_forward()
        right_cell = guard.whats_on_the_right()

        try:
            forward_free = _get_cell_from(map, *forward_cell) != BLOCKED
        except IndexError:
            # reached the border of the map
            forward_free = False

        try:
            right_free = _get_cell_from(map, *right_cell) != BLOCKED
        except IndexError:
            # reached the border of the map
            right_free = False


def _count_the_visited_cells(guard: Guard, map: Map) -> int:
    _move_the(guard, map)
    return guard.distinct_cell_visited


if __name__ == "__main__":
    main()

# > 2161
