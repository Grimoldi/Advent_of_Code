import sys

from loguru import logger

import data_loader

FILENAME = "03_input"
LEVEL = "DEBUG"
# LEVEL = "INFO"

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    level=LEVEL,
)


def first_question(filename=FILENAME) -> None:
    """Function to solve the first question."""


def second_question(filename=FILENAME) -> None:
    """Function to solve the second question."""


def _sum_bank_joltage(filename: str) -> int:
    """From a filename compute the sum of the joltage."""
    data = data_loader.load_input_data(filename)
    _sum = 0
    for battery in data:
        _sum += _find_bank_joltage([int(x) for x in battery])
    return _sum


def _find_bank_joltage(battery: list[int]) -> int:
    """
    Get the maximum joltage from a bank of batteries.

    eg.
    bank 987654321111111
    produces 98 joltage (9 and 8)
    """
    index_max = 0
    value_max = battery[0]

    for index, value in enumerate(battery):
        # we need at least two batteries
        if index == len(battery[:-1]):
            continue

        if value > value_max:
            value_max = value
            index_max = index

    second_battery = battery[index_max + 1 :]
    second_value_max = second_battery[0]

    for index, value in enumerate(second_battery):
        if value > second_value_max:
            second_value_max = value

    return value_max * 10 + second_value_max


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
