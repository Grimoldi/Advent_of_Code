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
            f"Currently in ({self.x},{self.y}), "
            f"moving forward with direction {self.direction}."
        )
        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        else:
            self.x -= 1
        logger.info(f"Now in ({self.x}, {self.y}).")

        self.steps += 1
        self._mark_cell_as_visited()

    def _mark_cell_as_visited(self) -> None:
        """Add to the visited cell the current cell."""
        self.visited_cell.add((self.x, self.y))

    def turn_right(self) -> None:
        """Turn the guard right 90 degree."""
        logger.info(f"Turning right from {self.direction}")
        next_direction = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }
        self.direction = next_direction[self.direction]
        logger.info(f"Now pointed to {self.direction}")

    def cell_ahead(self) -> tuple[int, int]:
        """Returns the position of the forward cell."""
        move = {
            Direction.UP: (self.x, self.y - 1),
            Direction.RIGHT: (self.x + 1, self.y),
            Direction.DOWN: (self.x, self.y + 1),
            Direction.LEFT: (self.x - 1, self.y),
        }

        return move[self.direction]

    def cell_on_the_right(self) -> tuple[int, int]:
        """Returns the position of the right cell."""
        right_cell = {
            Direction.UP: (self.x + 1, self.y),
            Direction.RIGHT: (self.x, self.y + 1),
            Direction.DOWN: (self.x - 1, self.y),
            Direction.LEFT: (self.x, self.y - 1),
        }
        return right_cell[self.direction]

    @property
    def distinct_cell_visited(self) -> int:
        """Return how many cell has visited."""
        return len(self.visited_cell)


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


def _get_cell_from(_map: Map, x: int, y: int) -> str:
    """Get the cell for a given position."""
    try:
        return list(_map[y])[x]
    except IndexError:
        return BLOCKED


def _move_the(guard: Guard, map: Map) -> None:
    """
    Move the guard:
     - forward if free
     - turn right if cannot proceed further
     - exit the map if unable to move forward or turn right
    """
    forward_cell = guard.cell_ahead()
    forward_free = _get_cell_from(map, *forward_cell) != BLOCKED
    right_cell = guard.cell_on_the_right()
    right_free = _get_cell_from(map, *right_cell) != BLOCKED

    while forward_free or right_free:
        if forward_free:
            guard.move_forward()
        else:
            guard.turn_right()
        forward_cell = guard.cell_ahead()
        right_cell = guard.cell_on_the_right()

        try:
            forward_free = _get_cell_from(map, *forward_cell) != BLOCKED
        except IndexError:
            # reached the border of the map
            logger.exception("Hit the border!")
            forward_free = False

        try:
            right_free = _get_cell_from(map, *right_cell) != BLOCKED
        except IndexError:
            # reached the border of the map
            logger.warning("Hit the border!")
            forward_free = False

    logger.info(f"Current cell ({guard.x}, {guard.y}), looking {guard.direction}.")
    try:
        logger.info(
            f"Cell ahead: {forward_cell=} {_get_cell_from(map, *forward_cell)}, "
            f"cell on the right {right_cell=} {_get_cell_from(map, *right_cell)}"
        )
    except IndexError:
        logger.info("Hit the border!")


def _count_the_visited_cells(guard: Guard, map: Map) -> int:
    _move_the(guard, map)
    return guard.distinct_cell_visited


if __name__ == "__main__":
    main()

# > 2161
# < 5552
