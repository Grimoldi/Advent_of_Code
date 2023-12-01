import itertools
import logging
import os
from typing import Any, Generator

import utils

DAY = os.path.basename(__file__).split(".")[0]


def get_couples(lines: list[str]) -> Generator[tuple[list[int], list[int]], None, None]:
    """Gets the data from the file and returns list of integers."""
    couples = _get_raw_couple(lines)
    index = 0
    while True:
        couple = couples[index]
        left: list = eval(couple[0])
        right: list = eval(couple[1])

        yield (left, right)
        index += 1


def _get_raw_couple(lines: list[str]) -> list[list[str]]:
    """Divide the lines in order to extract only contiguous couples."""
    couples_cardinality = len(lines) // 3 + 1
    couples = list()

    for index in range(couples_cardinality):
        starting = index * 3
        ending = (index + 1) * 3 - 1
        couples.append(lines[starting:ending])
    return couples


def compare_lists(first: list[int], second: list[int]) -> bool:
    """Compares the two lists and returns if they are in the right order."""
    logger = logging.getLogger(utils.LOGGER_NAME)
    logger.debug(f"\tcompare_lists: considering {first} : {second}")
    easy_list_discard = not (compare_lists_len(first, second))
    if easy_list_discard:
        return False
    is_correct_order = True
    zipped = itertools.zip_longest(first, second)
    for left, right in zipped:
        logger.debug(f"\tcompare_lists for loop: considering {left} : {right}")
        left_is_exhausted = compare_none_values(left)
        if left_is_exhausted:
            return True
        right_is_exhausted = compare_none_values(right)
        if right_is_exhausted:
            return False

        both_integers = isinstance(left, int) and isinstance(right, int)
        both_list = isinstance(left, list) and isinstance(right, list)
        left_int = isinstance(left, int)
        right_int = isinstance(right, int)

        if both_integers:
            logger.debug(f"\tboth integers")
            is_correct_order = compare_numbers(left, right)  # type: ignore
        elif left_int:
            logger.debug(f"\tleft integers, right list")
            first_int = find_nested_int(right)  # type: ignore
            if first_int is None:
                is_correct_order = False
            else:
                is_correct_order = compare_numbers(left, first_int)
        elif right_int:
            logger.debug(f"\tleft list, right integers")
            first_int = find_nested_int(left)  # type: ignore
            if first_int is None:
                is_correct_order = True
            else:
                is_correct_order = compare_numbers(first_int, right)
        elif both_list:
            logger.debug(f"\tboth lists")
            is_correct_order = compare_lists(left, right)
        else:
            raise ValueError(f"Something wrong happenend.")

        if not is_correct_order:
            break

    return is_correct_order


def compare_lists_len(left: list[Any], right: list[Any]) -> bool:
    """Compares the lens of the lists to find easy discardable lists."""
    logger = logging.getLogger(utils.LOGGER_NAME)
    if len(left) == 0 and len(right) > 0:
        logger.debug(f"\tLeft empty, right not empty")
        return True
    elif len(left) > 0 and len(right) == 0:
        logger.debug(f"\tRight empty, left not empty")
        return False
    elif len(left) > len(right):
        logger.debug(f"\tRight shorter then left.")
        return False
    else:
        return True


def compare_none_values(element: int | list[Any] | None) -> bool:
    """Checks if a an element is exausted."""
    if element is None:
        return True
    return False


def compare_numbers(left: int, right: int) -> bool:
    """Compares two numbers."""
    logger = logging.getLogger(utils.LOGGER_NAME)
    logger.debug(
        f"\tcompare_numbers: considering {left} {right}. Is left le right? {left <= right}"
    )
    return left <= right


def find_nested_int(listed: list[Any]) -> int | None:
    """Finds the first nested int."""
    if len(listed) == 0:
        return None

    if isinstance(listed[0], int):
        return listed[0]
    return find_nested_int(listed[0])


def load_data(
    debug: bool = False,
) -> tuple[int, Generator[tuple[list[int], list[int]], None, None]]:
    """Loads the data from the file."""
    lines = utils.load_input_data(DAY, debug)
    blocks = len(lines) // 3 + 1
    gen = get_couples(lines)
    return blocks, gen


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    blocks, gen = load_data(debug)
    logger = utils.setup_logger(utils.create_log_level(debug))
    sum = 0
    indexes = list()

    for index in range(blocks):
        left, right = next(gen)
        is_right_order = compare_lists(left, right)
        couple_index = index + 1
        if is_right_order:
            sum += couple_index
            indexes.append(couple_index)
        logger.info(f"\t{couple_index}: {left} {right} {is_right_order}\n")
    print(f"First question answer. The sum is: {sum} from indexs {indexes}.")


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    logger = utils.setup_logger(utils.create_log_level(debug))
    print(f"Second question answer.")


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
