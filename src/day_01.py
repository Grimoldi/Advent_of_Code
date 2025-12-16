import sys

from loguru import logger

import data_loader

FILENAME = "01_input"
LEFT = "L"
RIGHT = "R"

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    level="DEBUG",
)


def first_question(filename=FILENAME) -> None:
    """Function to solve the first question."""
    instructions = data_loader.load_input_data(filename)
    counted_zeros = _rotate_dial(instructions)

    print(f"First question answer. The counted number of '0' is: {counted_zeros}")


def second_question(filename=FILENAME) -> None:
    """Function to solve the second question."""
    instructions = data_loader.load_input_data(filename)
    counted_zeros = _rotate_dial_secure_password(instructions)

    print(f"Second question answer. The counted number of '0' is: {counted_zeros}")


def _rotate_dial(
    instructions: list[str],
    starting_number: int = 50,
) -> int:
    """Rotate the dial according to the instruction, return the number of time 0 is hit."""
    zeros = 0
    logger.debug(f"Starting at {starting_number}.")
    dial_number = starting_number

    for instruction in instructions:
        direction, delta = _get_detailed_instruction(instruction)

        if direction == "L":
            _, dial_number = _turn_left(dial_number, delta)
        else:
            _, dial_number = _turn_rigt(dial_number, delta)

        if dial_number == 0:
            zeros += 1

        logger.debug(
            f"Dial is now at {dial_number}, counted {zeros} 0, last instruction was {instruction}."
        )

    return zeros


def _rotate_dial_secure_password(
    instructions: list[str],
    starting_number: int = 50,
) -> int:
    """Rotate the dial according to the instruction, return the number of time 0 is hit."""
    zeros = 0
    logger.debug(f"Starting at {starting_number}.")
    dial_number = starting_number

    for index, instruction in enumerate(instructions):
        direction, delta = _get_detailed_instruction(instruction)
        starting_dial = dial_number

        if direction == "L":
            counted_zero_dialing, dial_number = _turn_left(dial_number, delta)
        else:
            counted_zero_dialing, dial_number = _turn_rigt(dial_number, delta)

        zeros += counted_zero_dialing
        if dial_number == 0:
            zeros += 1

        logger.debug(
            f"After instruction {index}: dial started at {starting_dial}, after {instruction} is now at {dial_number}; till now counted {zeros} '0'."
        )

    return zeros


def _get_detailed_instruction(instruction: str) -> tuple[str, int]:
    """Separate the direction from the number."""
    direction = instruction[0]
    delta = instruction[1:]

    return (direction, int(delta))


def _turn_left(starting: int, delta: int) -> tuple[int, int]:
    """Turn the dial left (subtract)."""
    ending = starting - delta
    zeros = 0
    # don't count first increment if starting from 0
    if starting == 0:
        zeros -= 1

    while ending < 0:
        ending += 100
        zeros += 1

    return zeros, ending


def _turn_rigt(starting: int, delta: int) -> tuple[int, int]:
    """Turn the dial right (add)."""
    ending = starting + delta
    zeros = 0
    while ending > 100:
        ending -= 100
        zeros += 1

    if ending == 100:
        ending = 0

    return zeros, ending


def main() -> None:
    # first_question()
    second_question()
    # 7243 too high


if __name__ == "__main__":
    main()
