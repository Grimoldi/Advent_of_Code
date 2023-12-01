import logging
import os
import re
import typing as ty
from dataclasses import dataclass, field
from enum import Enum

import utils

DAY = os.path.basename(__file__).split(".")[0]


@dataclass
class Beacon:
    x: int
    y: int


@dataclass
class Sensor:
    x: int
    y: int
    radius: int = field(init=False)

    def set_radius(self, beacon: Beacon) -> None:
        """Setter method."""
        self.radius = abs(beacon.x - self.x) + abs(beacon.y - self.y)


# doubles beacon, I know. But this dataclass is hashable for the set.
@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


'''
class CellStatus(Enum):
    BEACON = "B"
    SENSOR = "S"
    EMPTY = "."
    COVERED = "#"

@dataclass
class Grid:
    origin: Point
    leftmost: Point
    debug: bool = False

    def __post_init__(self) -> None:
        # will use range, so include right margin
        self.height = self.leftmost.y - self.origin.y + 1
        self.width = self.leftmost.x - self.origin.x + 1

        self.grid = [[CellStatus.EMPTY] * self.height for _ in range(self.width)]
        print(f"width: {len(self.grid)}, height: {len(self.grid[0])}")

        # grid will always start at (0, 0)
        self._x_shift = abs(min(self.origin.x, 0))
        self._y_shift = abs(min(self.origin.y, 0))

    def place_sensors(self, sensors: list[Sensor]) -> None:
        """Draws sensors on the grid."""
        for sensor in sensors:
            x = sensor.x + self._x_shift
            y = sensor.y + self._y_shift
            self.grid[x][y] = CellStatus.SENSOR

    def place_beacons(self, beacons: list[Beacon]) -> None:
        """Draws beacons on the grid."""
        for beacon in beacons:
            x = beacon.x + self._x_shift
            y = beacon.y + self._y_shift
            self.grid[x][y] = CellStatus.BEACON

    def place_coverage(self, sensors: list[Sensor]) -> None:
        """Draws cell coverage."""
        for sensor in sensors:
            self._cover_from_sensor(sensor)

    def _cover_from_sensor(self, sensor: Sensor) -> None:
        """Draws the coverage for a specific sensor."""
        cols = range(
            max(sensor.x - sensor.radius, 0),
            min(sensor.x + sensor.radius, self.leftmost.x) + self._x_shift + 1,
        )
        rows = range(
            max(sensor.y - sensor.radius, 0),
            min(sensor.y + sensor.radius, self.leftmost.y) + self._y_shift + 1,
        )
        sensor_point = Point(sensor.x + self._x_shift, sensor.y + self._y_shift)

        for x in cols:
            for y in rows:
                point = Point(x, y)
                is_in_radius = (
                    self._calculate_distance(sensor_point, point) <= sensor.radius
                )
                if is_in_radius:
                    try:
                        current_sign = self.grid[x][y]
                        if current_sign == CellStatus.EMPTY:
                            self.grid[x][y] = CellStatus.COVERED

                    except IndexError:
                        pass  # out of the grid, don't care

    def _calculate_distance(self, sensor: Point, point: Point) -> int:
        """Calculate the distance between two point."""
        return abs(sensor.x - point.x) + abs(sensor.y - point.y)

    def print_grid(self) -> None:
        """Prints the grid."""
        for row in range(self.height):
            print(str(row).zfill(2), end=" ")
            for col in range(self.width):
                print(self.grid[col][row].value, end=" ")
            print()

    def find_covered_cell_in_row(self, row: int) -> int:
        """Returns how many cells cannot a beacon be present in a given row."""
        cells = [col[row] for col in self.grid]
        return len([x for x in cells if x == CellStatus.COVERED])


def get_dimensions(
    sensors: list[Sensor], beacons: list[Beacon]
) -> tuple[int, int, int, int]:
    """Gets the origin and topleftmost point among sensors and beacons."""
    s_ox = min([sensor.x for sensor in sensors])
    b_ox = min([beacon.x for beacon in beacons])
    s_oy = min([sensor.y for sensor in sensors])
    b_oy = min([beacon.y for beacon in beacons])
    s_tx = max([sensor.x for sensor in sensors])
    b_tx = max([beacon.x for beacon in beacons])
    s_ty = max([sensor.y for sensor in sensors])
    b_ty = max([beacon.y for beacon in beacons])

    return (min(s_ox, b_ox), min(s_oy, b_oy), max(s_tx, b_tx), max(s_ty, b_ty))
'''


def load_sensors_and_beacons(debug: bool = False) -> tuple[list[Sensor], list[Beacon]]:
    """Load the input data and returns the beacons and the sensors."""
    data = utils.load_input_data(DAY, debug)
    beacons = list()
    sensors = list()
    for line in data:
        sensor, beacon = _create_sensor_and_beacon(line)
        sensors.append(sensor)
        beacons.append(beacon)

    return (sensors, beacons)


def _create_sensor_and_beacon(line: str) -> tuple[Sensor, Beacon]:
    """Loads a single sensor and beacon from a line."""
    data_compiler = re.compile(
        r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)$"
    )
    regex_groups = data_compiler.search(line)
    if not regex_groups:
        raise ValueError(f"Unable to find groups in line {line}")

    sensor = Sensor(
        int(regex_groups.group("sensor_x")),
        int(regex_groups.group("sensor_y")),
    )
    beacon = Beacon(
        int(regex_groups.group("beacon_x")),
        int(regex_groups.group("beacon_y")),
    )
    sensor.set_radius(beacon)
    return (sensor, beacon)


def get_busy_point(sensors: list[Sensor], beacons: list[Beacon]) -> list[Point]:
    """Convert sensors and beacons to points."""
    points = list()
    points.extend([Point(s.x, s.y) for s in sensors])
    points.extend([Point(b.x, b.y) for b in beacons])
    return points


def create_covered_points(
    sensors: list[Sensor], y: int, busy_points: list[Point], x: int | None = None
) -> set[Point]:
    """Creates the covered points.

    Enanchment after the prod run: instead of running a range check each sensor,
    should build the intersection of the ranges in order to analize them only once.
    """
    ranges = list()
    logger = logging.getLogger(utils.LOGGER_NAME)
    for index, sensor in enumerate(sensors):
        logger.debug(f"Analizying {index + 1}/{len(sensors)} sensor.")
        width = _calculate_points_in_range(sensor, y=y)
        logger.debug(f"Sensor {index + 1}: found {width} points.")
        if not _is_subset_of_range(ranges, width):  # type: ignore
            ranges.append(width)

    return _cover_ranges(ranges, y, busy_points)


def _calculate_points_in_range(
    sensor: Sensor, x: int | None = None, y: int | None = None
) -> ty.Iterable[int]:
    """Calculates the points within range.

    s = sensor
    |x - xs| + |y - ys| <= r
    |x - xs| <= r - |y - ys|
    |y - ys| - r <= x - xs <= r - |y-ys|
    |y - ys| - r + xs <= x <= r - |y-ys| + xs
    """
    if x:
        left_end = abs(sensor.x - x) - sensor.radius + sensor.y
        right_end = sensor.radius - abs(sensor.x - x) + sensor.y
        return range(min(left_end, right_end), max(left_end, right_end) + 1)
    if y:
        left_end = abs(sensor.y - y) - sensor.radius + sensor.x
        right_end = sensor.radius - abs(sensor.y - y) + sensor.x
        return range(min(left_end, right_end), max(left_end, right_end) + 1)
    else:
        raise ValueError("Unable to find the range.")


def _is_subset_of_range(
    ranges: list[ty.Iterator[int]], width: ty.Iterator[int]
) -> bool:
    """Checks if a range is already listed in ranges."""
    is_subset = False
    for _range in ranges:
        left_cover = _range[0] < width[0]  # type: ignore
        right_cover = _range[-1] > width[-1]  # type: ignore
        if right_cover and left_cover:
            is_subset = True
            break
    return is_subset


def _cover_ranges(
    ranges: list[ty.Iterator[int]], y: int, busy_points: list[Point]
) -> set[Point]:
    """Return the covered points."""
    covered = set()
    for width in ranges:
        for x in width:
            point = Point(x, y)
            if point not in busy_points:
                covered.add(point)

    return covered


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    sensors, beacons = load_sensors_and_beacons(debug)
    logger = utils.setup_logger(utils.create_log_level(debug))
    busy_points = get_busy_point(sensors, beacons)
    if debug:
        y = 10
    else:
        y = 20_000
    covered = create_covered_points(sensors, y, busy_points)

    print(f"First question answer. Busy points on row {y} are: {len(covered)}.")


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    logger = utils.setup_logger(utils.create_log_level(debug))
    print(f"Second question answer.")


def main() -> None:
    first_question(True)
    second_question()


if __name__ == "__main__":
    main()
