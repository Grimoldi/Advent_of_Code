import os
from dataclasses import dataclass
from enum import Enum

from utils import load_input_data

DAY = os.path.basename(__file__).split(".")[0]


class Cell(Enum):
    ROCK = "#"
    SAND = "o"
    AIR = "."


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Segment:
    starting_point: Point
    ending_point: Point


@dataclass
class Grid:
    width: int
    height: int
    altitude: int
    debug: bool = False

    def __post_init__(self) -> None:
        self.grid = [[Cell.AIR] * self.height for _ in range(self.width)]
        self._sand = Point(500, 0)
        self._center_move = self._left_move = self._right_move = 0
        self._repeat = 0

    def set_altitude(self, altitude: int) -> None:
        """Setter method."""
        self.altitude = altitude

    def draw_rock_segment(self, start: Point, end: Point) -> None:
        """Draws a rock segment on the grid."""
        width = end.x - start.x
        height = end.y - start.y

        if height == 0:
            starting_col, ending_col = self._get_entremity_coordinates(end.x, start.x)
            for col in range(starting_col, ending_col + 1):
                if self.debug:
                    print(f"\tFilling col ({col}, {start.y}) with rock.")
                self.grid[col][start.y] = Cell.ROCK

        else:
            starting_row, ending_row = self._get_entremity_coordinates(end.y, start.y)
            for row in range(starting_row, ending_row + 1):
                if self.debug:
                    print(f"\tFilling row ({start.x}, {row}) with rock.")
                self.grid[start.x][row] = Cell.ROCK

    def _get_entremity_coordinates(
        self, coordinate_1: int, coordinate_2: int
    ) -> tuple[int, int]:
        """Gets the starting and the ending point in order."""
        if coordinate_1 > coordinate_2:
            return (coordinate_2, coordinate_1)
        return (coordinate_1, coordinate_2)

    def sand_turn(self) -> None:
        """A unit of sand falls down."""
        if self._check_below_center_cell():
            self._move_sand_below_center()
            self.sand_turn()

        elif self._check_below_left_cell():
            self._move_sand_below_left()
            self.sand_turn()

        elif self._check_below_right_cell():
            self._move_sand_below_right()
            self.sand_turn()

        elif self._find_if_blocked():
            raise IndexError("Sand spawning point is blocked.")

        else:
            self._reset_sand()
            return

    def _check_below_center_cell(self) -> bool:
        """Checks one cell under."""
        new_x = self._sand.x
        new_y = self._sand.y + 1

        if self.grid[new_x][new_y] != Cell.AIR:
            if self.debug:
                print(f"Unable to move sand to ({new_x}, {new_y}).")
            return False
        return True

    def _move_sand_below_center(self) -> None:
        """Move sand one cell under."""
        new_x = self._sand.x
        new_y = self._sand.y + 1
        self._move_sand_sign(new_x, new_y)
        self._center_move += 1

    def _check_below_left_cell(self) -> bool:
        """Checks one cell under and one cell left."""
        new_x = self._sand.x - 1
        new_y = self._sand.y + 1

        if self.grid[new_x][new_y] != Cell.AIR:
            if self.debug:
                print(f"Unable to move sand to ({new_x}, {new_y}).")
            return False
        return True

    def _move_sand_below_left(self) -> None:
        """Move sand one cell under left."""
        new_x = self._sand.x - 1
        new_y = self._sand.y + 1
        self._move_sand_sign(new_x, new_y)
        self._left_move += 1

    def _check_below_right_cell(self) -> bool:
        """Checks one cell under and one cell right."""
        new_x = self._sand.x + 1
        new_y = self._sand.y + 1

        if self.grid[new_x][new_y] != Cell.AIR:
            if self.debug:
                print(f"Unable to move sand to ({new_x}, {new_y}).")
            return False
        return True

    def _move_sand_below_right(self) -> None:
        """Move sand one cell under right."""
        new_x = self._sand.x + 1
        new_y = self._sand.y + 1
        self._move_sand_sign(new_x, new_y)
        self._right_move += 1

    def _reset_sand(self) -> None:
        """Reset sand to it's starting point."""
        self._move_sand(500, 0)
        self._right_move = self._center_move = self._left_move = 0

    def _move_sand_sign(self, x: int, y: int) -> None:
        """Moves the sand sign."""
        if self.debug:
            print(
                f"Moving sand sign from ({self._sand.x}, {self._sand.y}) to ({x}, {y})."
            )
        self._draw_air(self._sand.x, self._sand.y)
        self._draw_sand(x, y)
        self._move_sand(x, y)

    def _find_if_blocked(self) -> bool:
        """Returns if the spawning point is blocked by sand."""
        left = self.grid[499][1]
        center = self.grid[500][1]
        right = self.grid[501][1]
        is_blocked = left == Cell.SAND and center == Cell.SAND and right == Cell.SAND
        if self.debug:
            print(f"Is blocked? {is_blocked}. {left=} {center=} {right=}")
        return is_blocked

    def _draw_sand(self, x: int, y: int) -> None:
        """Draws a sand."""
        self.grid[x][y] = Cell.SAND

    def _draw_air(self, x: int, y: int) -> None:
        """Draws air."""
        self.grid[x][y] = Cell.AIR

    def _move_sand(self, x: int, y: int) -> None:
        """Move the unit of sand on the grid."""
        self._sand = Point(x, y)

    def print_example_q1(self) -> None:
        """Print the example."""
        if self.debug:
            row_range = range(10)
            col_range = range(494, 504)
        else:
            row_range = range(400, 550)
            col_range = range(50, 160)
        for row in row_range:
            print(row, end=" ")
            for col in col_range:
                print(self.grid[col][row - 1].value, end=" ")
            print()

    def print_example_q2(self) -> None:
        """Print the example."""
        if self.debug:
            row_range = range(13)
            col_range = range(487, 513)
        else:
            row_range = range(160)
            col_range = range(400, 550)
        for row in row_range:
            print(row, end=" ")
            for col in col_range:
                if col == 500 and row == 0:
                    print("+", end=" ")
                else:
                    print(self.grid[col][row].value, end=" ")
            print()


def setup_grid(debug: bool = False) -> Grid:
    """Sets up the grid instance."""
    if debug:
        grid = Grid(514, 13, 0, debug)
    else:
        grid = Grid(1000, 500, 0, debug)
    return grid


def load_segments(debug: bool = False) -> list[list[Point]]:
    """Gets the segments from the input file."""
    data = load_input_data(DAY, debug)
    contiguos_segments = list()
    for line in data:
        segments = list()
        for segment in line.split("->"):
            x, y = segment.strip().split(",")
            new_point = Point(int(x), int(y))
            segments.append(new_point)
        contiguos_segments.append(segments)

    return contiguos_segments


def write_rock_segments(grid: Grid, all_segments: list[list[Point]]) -> None:
    """Writes the rocks on the grid."""
    for segments in all_segments:
        for index, segment in enumerate(segments):
            start_from = segment
            try:
                end_to = segments[index + 1]
            except IndexError:
                break
            grid.draw_rock_segment(start_from, end_to)


def find_highest_point(all_segments: list[list[Point]]) -> int:
    """Finds the highest point."""
    altitudes = list()
    for segments in all_segments:
        for segment in segments:
            altitudes.append(segment.y)

    altitudes = sorted(altitudes, reverse=True)
    return altitudes[0]


def draw_floor(grid: Grid, altitude: int) -> None:
    """Draws the floor."""
    y = 2 + altitude
    leftmost_point = Point(0, y)
    rightmost_point = Point(grid.width - 1, y)
    grid.draw_rock_segment(leftmost_point, rightmost_point)


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    grid = setup_grid(debug)
    all_segments = load_segments(debug)
    write_rock_segments(grid, all_segments)

    if debug:
        grid.print_example_q1()

    unit_of_sand = 0
    while True:
        unit_of_sand += 1
        if debug:
            print(f"\n\nUnit of sand: {unit_of_sand}")
        try:
            grid.sand_turn()
            if debug:
                grid.print_example_q1()
        except IndexError:
            unit_of_sand -= 1
            break
    print(
        f"First question answer. The unit of sand necessary to fullfill are: {unit_of_sand}"
    )


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    grid = setup_grid(debug)
    all_segments = load_segments(debug)
    write_rock_segments(grid, all_segments)
    altitude = find_highest_point(all_segments)
    draw_floor(grid, altitude)
    grid.set_altitude(altitude)

    if debug:
        grid.print_example_q2()

    unit_of_sand = 0
    while True:
        unit_of_sand += 1
        if debug:
            print(f"\n\nUnit of sand: {unit_of_sand}")
        try:
            grid.sand_turn()
            if debug:
                grid.print_example_q2()
        except IndexError as e:
            print(e)
            unit_of_sand += 1
            break
        if debug and unit_of_sand == 100:
            break
    print(
        f"Second question answer. The unit of sand necessary to fullfill are: {unit_of_sand}"
    )


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
