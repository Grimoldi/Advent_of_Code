import os
from dataclasses import dataclass
from enum import Enum, auto

import utils

DAY = os.path.basename(__file__).split(".")[0]
MAX_CLOCKS = 220
CRT_WIDTH = 40
CRT_RESOLUTION = 240
INTERESTING_CLOCKS = [20, 60, 100, 140, 180, 220]


class Operation(Enum):
    PASS = auto()
    ADD = auto()


@dataclass
class Move:
    operation: Operation
    value: int


@dataclass
class ElvesCPU:
    def __post_init__(self) -> None:
        self._register_value = 1
        self._internal_cycle = 1
        self._value = 0
        self._add_on_cycle = -1
        self._busy = False

    def _pass(self) -> None:
        """Pass operation."""
        self._busy = True

    def _add_value(self, value: int) -> None:
        """Set up for an adding operation."""
        self._add_on_cycle = self._internal_cycle + 1
        self._value = value
        self._busy = True

    def make_move(self, move: Move) -> None:
        """Performs a move."""
        if move.operation == Operation.PASS:
            self._pass()
        elif move.operation == Operation.ADD:
            self._add_value(move.value)

    def perform_clock(self) -> None:
        """Performs a clock cycle."""
        self._internal_cycle += 1
        if self._internal_cycle - 1 == self._add_on_cycle:
            self._register_value += self._value
            self._busy = False

    def get_cycle(self) -> int:
        """Getter method."""
        return self._internal_cycle

    def get_register_value(self) -> int:
        """Getter method."""
        return self._register_value

    def get_busy(self) -> bool:
        """Getter method."""
        return self._busy

    def free_cpu(self) -> None:
        self._busy = False


def get_move(line: str) -> Move:
    """From the raw line gets a Move instance."""
    try:
        _, value = line.split(" ")
        return Move(Operation.ADD, int(value))
    except ValueError as e:
        return Move(Operation.PASS, 0)


def get_moves(debug: bool = False) -> list[Move]:
    """Gets the moves from the input file."""
    data = utils.load_input_data(DAY, debug)
    moves = list()
    for line in data:
        moves.append(get_move(line))

    return moves


def print_crt(cycle: int, register_value: int, debug: bool = False) -> None:
    """Prints a # or a . on the screen."""
    horizontal_position = cycle - ((cycle // CRT_WIDTH) * CRT_WIDTH) - 1
    is_sprite_in_position = (
        horizontal_position - 1 <= register_value <= horizontal_position + 1
    )
    if is_sprite_in_position:
        print("#", end="")
    else:
        print(".", end="")
    if False:
        print(
            f"{cycle=} {horizontal_position=} {register_value=} {is_sprite_in_position=}"
        )
    if cycle % CRT_WIDTH == 0:
        print()


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    moves = get_moves(debug)
    logger = utils.setup_logger(utils.create_log_level(debug))
    cpu = ElvesCPU()
    intersting_values = list()
    stop = False
    for index, move in enumerate(moves):
        # print(f"{move.operation.name}")
        is_busy = cpu.get_busy()
        while is_busy:
            # loop operations
            cpu.perform_clock()
            if moves[index - 1].operation == Operation.PASS:
                cpu.free_cpu()
            is_busy = cpu.get_busy()

            # values operations
            cycle = cpu.get_cycle()
            register_value = cpu.get_register_value()
            logger.debug(f"{cycle=} {register_value=}")

            if cycle == MAX_CLOCKS + 1:
                stop = True
                break
            if cycle in INTERESTING_CLOCKS:
                intersting_values.append(cycle * register_value)
                logger.debug(f"{cycle}, {register_value} {intersting_values[-1]}")
        if stop:
            break

        cpu.make_move(move)
    print(
        f"First question answer. The sum of the interesting values is: {sum(intersting_values)}"
    )


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    moves = get_moves(debug)
    cpu = ElvesCPU()
    stop = False
    for index, move in enumerate(moves):
        is_busy = cpu.get_busy()
        while is_busy:
            # values operations
            cycle = cpu.get_cycle()
            register_value = cpu.get_register_value()
            print_crt(cycle, register_value, True)

            # loop operations
            cpu.perform_clock()
            if moves[index - 1].operation == Operation.PASS:
                cpu.free_cpu()
            is_busy = cpu.get_busy()

            if cycle == CRT_RESOLUTION:
                stop = True
                break

        if stop:
            break

        cpu.make_move(move)


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
