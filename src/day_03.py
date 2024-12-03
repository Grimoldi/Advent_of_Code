import os
import re

import utils

DAY = os.path.basename(__file__).split(".")[0]
FILENAME = "03_first"
logger = utils.setup_logger(utils.create_log_level(False))


def first_question() -> None:
    """Function to solve the first question."""
    print(
        "First question answer. " f"The sum is: {_calculate_total_sum_from(FILENAME)}"
    )


def second_question() -> None:
    """Function to solve the second question."""
    print(
        "Second question answer. "
        f"The sum is: {_calculate_total_sum_of_enabled_instructions_from(FILENAME)}"
    )


def main() -> None:
    first_question()
    second_question()


def _build_data_from(filename: str) -> list[str]:
    """Search on the input file for only the mul(x,y) strings."""
    raw_data = utils.load_input_data(filename)
    oneline_data = "".join(raw_data)

    return _extract_string_mul_couple_from(oneline_data)


def _extract_string_mul_couple_from(data: str) -> list[str]:
    """Extract all the 'mul(x,y)' from a string."""
    mul_regex = r"mul\(\d+\,\d+\)"
    return re.findall(mul_regex, data)


def _multiply_couple(mul_string: str) -> int:
    """From a string couple, calculates the product."""
    mul_string = mul_string.replace("mul(", "")
    mul_string = mul_string.replace(")", "")
    x, y = [int(x) for x in mul_string.split(",")]

    return x * y


def _calculate_total_sum_from(filename: str) -> int:
    """Given the filename, get the total of the correct operations."""
    couples = _build_data_from(filename)
    total = 0
    for couple in couples:
        total += _multiply_couple(couple)

    return total


def _build_enabled_data_from(filename: str) -> list[str]:
    """Search on the input file for only the enabled instructions."""
    """
    Strategy:
        we have like
        <enabled operations>[DONT<disabled operations>|DO<enabled operations>]*
        
        split the string by don't()
        - the first part will be the default enabled operation(s)
        - all other parts will be like <disable operations>DO<enabled operations>[DO<enabled operations>]*

        then split by DO
        - the first part will contain the disabled operation(s), just discard them
        - the second (and latter parts if any) will only have enabled operation(s)
    """
    DONT = "don't()"
    DO = "do()"
    raw_data = utils.load_input_data(filename)
    oneline_data = "".join(raw_data)
    enabled_instructions: list[str] = list()

    logger.debug(oneline_data)

    first_split = oneline_data.split(DONT)
    logger.debug(f"ADDING First enabled operation: {first_split[0]}")
    enabled_instructions.append(first_split[0])  # first instruction is always enabled

    for instruction in first_split[1:]:
        logger.debug(f"LOOKING in {instruction}")
        if DO not in instruction:
            logger.info("Didn't find enabled instruction, skipping")
            continue

        second_split = instruction.split(DO)
        # instruction AFTER the split are enabled
        # insert ALL operations (in case of multiple consecutive DO)
        enabled_instructions.extend(second_split[1:])

    mul_enabled_operations: list[str] = list()
    for instruction in enabled_instructions:
        mul_enabled_operations.extend(_extract_string_mul_couple_from(instruction))

    return mul_enabled_operations


def _calculate_total_sum_of_enabled_instructions_from(filename: str) -> int:
    """Given the filename, get the total of the enabled operations."""
    couples = _build_enabled_data_from(filename)
    total = 0
    for couple in couples:
        total += _multiply_couple(couple)

    return total


if __name__ == "__main__":
    main()
