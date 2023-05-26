import os
import string

import utils

DAY = os.path.basename(__file__).split(".")[0]


def split_items_per_compartment(items: str) -> tuple[str, str]:
    """Splits the items between the two compartments."""
    capacity = len(items)
    first = items[0 : capacity // 2]
    second = items[capacity // 2 : capacity]

    return (first, second)


def find_duplicate_item(first: str, second: str) -> str:
    """Finds the duplicate item between the two compartments."""
    duplicate = ""
    for item in first:
        if item in second:
            duplicate = item

    return duplicate


def calculate_weigth(item: str) -> int:
    """Calculate the weigth for each item."""
    mapping = dict(zip(string.ascii_lowercase, range(1, 27)))
    if item in mapping:
        return mapping[item]
    else:
        return mapping[item.lower()] + 26


def find_group_badge(rucksacks: list[str]) -> str:
    """Find the common item among a group."""
    badge = ""
    for item in rucksacks[0]:
        if item in rucksacks[1] and item in rucksacks[2]:
            badge = item
            break
    return badge


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    rucksacks = utils.load_input_data(DAY, debug)
    logger = utils.setup_logger(utils.create_log_level(debug))

    total_weigth = 0
    for rucksack_item in rucksacks:
        first, second = split_items_per_compartment(rucksack_item)
        duplicate_item = find_duplicate_item(first, second)
        weigth = calculate_weigth(duplicate_item)

        total_weigth += weigth

        logger.debug(f"{first=}, {second=}, {duplicate_item=}, {weigth=}")

    logger.info(f"Total priority for first question: {total_weigth}")


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    rucksacks = utils.load_input_data(DAY, debug)
    logger = utils.setup_logger(utils.create_log_level(debug))

    total_weigth = 0
    groups = len(rucksacks) // 3
    index = 0
    while index < groups:
        starting_pos = index * 3
        finishing_pos = (index + 1) * 3
        group_rucksacks = rucksacks[starting_pos:finishing_pos]
        group_badge = find_group_badge(group_rucksacks)
        weigth = calculate_weigth(group_badge)

        total_weigth += weigth
        index += 1

        logger.debug(f"{group_rucksacks=}, {group_badge=}, {weigth=}")

    logger.info(f"Total priority for second question: {total_weigth}")


def main() -> None:
    first_question(True)
    second_question()


if __name__ == "__main__":
    main()
