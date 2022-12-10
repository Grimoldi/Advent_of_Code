import os
from dataclasses import dataclass, field
from enum import Enum, auto

from utils import load_input_data

DAY = os.path.basename(__file__).split(".")[0]


@dataclass
class Position:
    """Dataclass for the position on the cartesian square."""

    x: int
    y: int

    def set_position(self, new_x: int, new_y: int) -> None:
        """Setter method"""
        self.x = new_x
        self.y = new_y


@dataclass
class Knot:
    """Dataclass for the Head and Tail knots."""

    name: str
    position: Position
    visited: set[tuple[int, int]] = field(default_factory=set)

    def update_position(self, x: int, y: int) -> None:
        """Update the position of a knot."""
        self.position.set_position(x, y)

    def get_position(self) -> Position:
        """Getter method."""
        return self.position

    def add_visited_point(self, pos: tuple[int, int]) -> None:
        """Setter method"""
        self.visited.add(pos)


class Direction(Enum):
    """Enum for the direction of the move."""

    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


@dataclass
class Move:
    """Represent a possible move of the knots."""

    direction: Direction
    steps: int


@dataclass
class Grid:
    """Represent the grid on which the knots will move."""

    def set_cell_to_visited(self, knot: Knot, debug: bool = False) -> None:
        """Sets a cell as visited."""
        pos = knot.get_position()
        knot.add_visited_point((pos.x, pos.y))
        if debug:
            print(f"{knot.name}: set {pos.x} {pos.y} cell to visited.")

    def calculate_distance(self, head: Knot, tail: Knot) -> tuple[int, int]:
        """Calculate the distance between the knots."""
        head_pos = head.get_position()
        tail_pos = tail.get_position()
        x_delta = abs(head_pos.x - tail_pos.x)
        y_delta = abs(head_pos.y - tail_pos.y)

        return (x_delta, y_delta)

    def move_head(self, direction: Direction, head: Knot) -> None:
        """Moves the head."""
        current_position = head.get_position()

        if direction == Direction.UP:
            head.update_position(current_position.x, current_position.y - 1)
        elif direction == Direction.DOWN:
            head.update_position(current_position.x, current_position.y + 1)
        elif direction == Direction.LEFT:
            head.update_position(current_position.x - 1, current_position.y)
        elif direction == Direction.RIGHT:
            head.update_position(current_position.x + 1, current_position.y)
        else:
            raise ValueError(f"Unable to move to the {direction.name}!")

    def move_tail(self, head: Knot, tail: Knot) -> None:
        """Moves the tail."""
        head_pos = head.get_position()
        tail_pos = tail.get_position()

        move_right = head_pos.x > tail_pos.x
        move_left = head_pos.x < tail_pos.x
        move_up = head_pos.y > tail_pos.y
        move_down = head_pos.y < tail_pos.y

        if move_right:
            self._move_right(tail)
        elif move_left:
            self._move_left(tail)

        if move_up:
            self._move_up(tail)
        elif move_down:
            self._move_down(tail)

    def _move_right(self, tail: Knot) -> None:
        """Move tail to the righ."""
        current_pos = tail.get_position()
        new_x = current_pos.x + 1
        tail.update_position(new_x, current_pos.y)

    def _move_left(self, tail: Knot) -> None:
        """Move tail to the left."""
        current_pos = tail.get_position()
        new_x = current_pos.x - 1
        tail.update_position(new_x, current_pos.y)

    def _move_up(self, tail: Knot) -> None:
        """Move tail to the up."""
        current_pos = tail.get_position()
        new_y = current_pos.y + 1
        tail.update_position(current_pos.x, new_y)

    def _move_down(self, tail: Knot) -> None:
        """Move tail to the down."""
        current_pos = tail.get_position()
        new_y = current_pos.y - 1
        tail.update_position(current_pos.x, new_y)


def get_move(line: str) -> Move:
    """From a raw move get a Move instance."""
    direction, steps = line.split(" ")
    mapping = {
        "U": Direction.UP,
        "D": Direction.DOWN,
        "L": Direction.LEFT,
        "R": Direction.RIGHT,
    }
    return Move(mapping[direction], int(steps))


def get_moves(debug: bool = False) -> list[Move]:
    """Get the moves from the data file."""
    data = load_input_data(DAY, debug)
    moves = list()
    for line in data:
        moves.append(get_move(line))

    return moves


def move_knots(head: Knot, tail: Knot, grid: Grid, debug: bool = False) -> None:
    """Move the knots."""
    dist_x, dist_y = grid.calculate_distance(head, tail)
    head_too_far = dist_y > 1 or dist_x > 1
    if head_too_far:
        grid.move_tail(head, tail)
        grid.set_cell_to_visited(tail, debug)


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    moves = get_moves(debug)
    starting_pos = {"x": 0, "y": 0}

    head = Knot("head", Position(**starting_pos))
    tail = Knot("tail", Position(**starting_pos))
    grid = Grid()
    grid.set_cell_to_visited(tail, debug)

    for move in moves:
        if debug:
            print(f"{move=}")
        for _ in range(move.steps):
            grid.move_head(move.direction, head)
            grid.set_cell_to_visited(head, debug)
            move_knots(head, tail, grid, debug)

    if debug:
        print(head.visited)
        print(tail.visited)
    print(
        f"First question answer. "
        f"The total position visited by the tail knot are: {len(tail.visited)}"
    )


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    moves = get_moves(debug)
    starting_pos = {"x": 0, "y": 0}

    head = Knot("head", Position(**starting_pos))
    k1 = Knot("k1", Position(**starting_pos))
    k2 = Knot("k2", Position(**starting_pos))
    k3 = Knot("k3", Position(**starting_pos))
    k4 = Knot("k4", Position(**starting_pos))
    k5 = Knot("k5", Position(**starting_pos))
    k6 = Knot("k6", Position(**starting_pos))
    k7 = Knot("k7", Position(**starting_pos))
    k8 = Knot("k8", Position(**starting_pos))
    tail = Knot("tail", Position(**starting_pos))

    grid = Grid()
    grid.set_cell_to_visited(tail)

    couples = [
        (head, k1),
        (k1, k2),
        (k2, k3),
        (k3, k4),
        (k4, k5),
        (k5, k6),
        (k6, k7),
        (k7, k8),
        (k8, tail),
    ]

    for move in moves:
        if debug:
            print(f"{move=}")
        for _ in range(move.steps):
            grid.move_head(move.direction, head)
            grid.set_cell_to_visited(head, debug)
            for temp_head, temp_tail in couples:
                move_knots(temp_head, temp_tail, grid, debug)

    if debug:
        print(head.visited)
        print(tail.visited)
    print(
        f"Second question answer. "
        f"The total position visited by the tail knot are: {len(tail.visited)}"
    )


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
