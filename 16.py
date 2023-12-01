from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from functools import partial
from pprint import PrettyPrinter

import utils

DAY = os.path.basename(__file__).split(".")[0]

pp = PrettyPrinter(indent=4, width=160)


@dataclass
class RawValve:
    name: str
    rate: int
    childs: list[str]


@dataclass
class Valve:
    name: str
    rate: int
    neighbours: list[Valve] = field(default_factory=list)
    is_open: bool = False

    def add_neighbour(self, node: Valve) -> None:
        self.neighbours.append(node)

    def get_neighbours(self) -> list[Valve]:
        return self.neighbours

    def set_visited(self) -> None:
        self.is_open = True

    @property
    def releseable_pressure(self) -> int:
        if self.is_open:
            return 0
        else:
            return self.rate

    def __repr__(self) -> str:
        return f"Valve(name={self.name}, rate={self.rate}, neighbours={[edge.name for edge in self.neighbours]})"


@dataclass
class ValveStrategy:
    valve: Valve
    distance: int
    max_pression: int


@dataclass
class ValveTraversePath:
    valves: list[Valve]
    pression_released: int = 0

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(utils.LOGGER_NAME)
        self._VALVE_OPENING_TIME = 1
        self._path: list[str] = list()

    def get_next_hop(self, starting: Valve, time: int) -> ValveStrategy:
        """Gets the next optimal valve to visit."""
        distance_matrix = self._build_matrix(starting, time)
        sorter = partial(self._sorter)
        distance_matrix.sort(key=sorter, reverse=True)
        pp.pprint(distance_matrix)

        return distance_matrix[0]

    def _sorter(self, value: ValveStrategy) -> int:
        """Sorts valve by the max pression releasable."""
        return value.max_pression

    def _build_matrix(self, starting: Valve, time: int) -> list[ValveStrategy]:
        """
        Builds an internal matrix with the minimum distance from a node.
        On first step, e.g., it will return:
        A: 0 (starting node)
        B: 1
        C: 2
        D: 1
        etc
        """
        visited_valves: list[ValveStrategy] = list()
        while len(visited_valves) != len(self.valves):
            # self._logger.debug(f"{len(visited_valves)=} {len(self.valves)=}")
            self._logger.info(f"Starting from {starting.name}")
            for current_valve in self.valves:
                # self._logger.debug(f"Considering {current_valve.name}")
                temp = None

                # current valve has a distance of 0 from itself
                if current_valve == starting:
                    distance = 0
                    pression = self._get_max_p(
                        distance, current_valve.releseable_pressure, time
                    )
                    temp = ValveStrategy(current_valve, distance, pression)

                # foreach visited valve find if current valved is close to any,
                # and find its minimum distance
                for visited_valve in visited_valves:
                    if current_valve in visited_valve.valve.get_neighbours():
                        """
                        self._logger.debug(
                            f"Valve {current_valve.name} is neighbour of {visited_valve.valve.name}"
                        )
                        """
                        distance = visited_valve.distance + 1
                        pression = self._get_max_p(
                            distance, current_valve.releseable_pressure, time
                        )
                        if not temp:
                            temp = ValveStrategy(current_valve, distance, pression)
                        elif temp.distance > distance:
                            temp = ValveStrategy(current_valve, distance, pression)

                # insert or update temp in visited_valves
                if (
                    current_valve not in [vv.valve for vv in visited_valves]
                    and temp is not None
                ):
                    visited_valves.append(temp)

                elif temp is not None:
                    for index, visited_valve in enumerate(visited_valves):
                        if (
                            visited_valve == temp
                            and temp.distance < visited_valve.distance
                        ):
                            visited_valves[index] = temp
        return visited_valves

    def _get_max_p(self, distance: int, rate: int, time: int) -> int:
        """Gets the max pressure realeasable, equal to pressure * (time - distance - time to open the valve)."""
        return (time - distance - self._VALVE_OPENING_TIME) * rate

    def visit_valve(self, valve: ValveStrategy, time: int) -> int:
        """Move to a valve and open it."""
        if valve.max_pression == 0:
            return 0

        time -= valve.distance + self._VALVE_OPENING_TIME
        self.pression_released += valve.max_pression
        self._logger.info(f"Released {valve.max_pression} unit of pressure.")
        valve.valve.set_visited()
        self._path.append(valve.valve.name)

        return time


def build_valves_from_scratch(debug: bool = False) -> list[Valve]:
    """From input file creates the nodes to traverse."""
    data = utils.load_input_data(DAY, debug)
    raw_valves = _parse_input_data(data)
    nodes = _build_valves(raw_valves)

    return nodes


def _parse_input_data(data: list[str]) -> list[RawValve]:
    """Parses the input data into a list of raw valves."""
    data_compiler = re.compile(
        r"Valve (?P<valve>\w+) has flow rate=(?P<rate>\d+)\; tunnels? leads? to valves? (?P<valves>.*)$"
    )
    raw_valves: list[RawValve] = list()

    for line in data:
        regex_groups = data_compiler.search(line)
        if regex_groups is None:
            raise ValueError(f"Unable to parse line {line}")

        groups = regex_groups.groupdict()
        valve = groups.get("valve")
        rate = groups.get("rate")
        valves = [valve.strip() for valve in groups.get("valves", "").split(",")]

        if valve is None or rate is None:
            raise ValueError(f"Unable to find elements in {line}")

        raw_valves.append(RawValve(valve, int(rate), valves))

    return raw_valves


def _build_valves(raw_valves: list[RawValve]) -> list[Valve]:
    valves: list[Valve] = list()
    for node in raw_valves:
        valves.append(Valve(node.name, node.rate))

    for node in valves:
        for raw_valve in raw_valves:
            if node.name == raw_valve.name:
                for edge in raw_valve.childs:
                    edge_node = _find_node_by_name(valves, edge)
                    node.add_neighbour(edge_node)
    return valves


def _find_node_by_name(nodes: list[Valve], name: str) -> Valve:
    """Get a valve by its name."""
    for node in nodes:
        if node.name == name:
            return node
    raise NameError(f"Unable to find a valve named {name}.")


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    logger = utils.setup_logger(utils.create_log_level(debug))
    valves = build_valves_from_scratch(debug)
    TIME = 30
    traverse = ValveTraversePath(valves)
    starting_valve = valves[0]
    elapsed_time = TIME
    while elapsed_time > 0:
        next_hop = traverse.get_next_hop(starting_valve, TIME)
        starting_valve = next_hop.valve
        logger.debug(f"Next hop will be {starting_valve.name}")
        logger.debug(f"Time before moving to {starting_valve.name} is {elapsed_time}.")
        elapsed_time = traverse.visit_valve(next_hop, elapsed_time)
        logger.debug(f"Time after moving to {starting_valve.name} is {elapsed_time}.")

    print(f"First question answer.")
    print(f"Maximum pressure released: {traverse.pression_released}")
    print(f"Traverse path walked: {traverse._path}")


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    logger = utils.setup_logger(utils.create_log_level(debug))
    print(f"Second question answer.")


def main() -> None:
    first_question(True)
    # 1949 too low
    second_question()


if __name__ == "__main__":
    main()
