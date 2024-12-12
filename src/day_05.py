import os

import utils

DAY = os.path.basename(__file__).split(".")[0]
FILENAME = "05_first"
logger = utils.setup_logger(utils.create_log_level(False))

Rule = tuple[int, int]
Page = int
Pages = list[Page]


def first_question() -> None:
    """Function to solve the first question."""
    rules, pages = _build_data_from(FILENAME)
    print(
        "First question answer. "
        f"The total sum is: {_calculate_sum_of_middlepages(pages, rules)}"
    )


def second_question() -> None:
    """Function to solve the second question."""
    print("Second question answer. ")


def main() -> None:
    first_question()
    second_question()


def _build_data_from(filename: str) -> tuple[list[Rule], list[Pages]]:
    """Build from the input file the rules and pages."""
    PIPE = "|"
    COMMA = ","
    data = utils.load_input_data(filename)
    rules: list[Rule] = list()
    pages: list[Pages] = list()
    for line in data:
        if PIPE in line:
            _rules = line.split(PIPE)
            rules.append((int(_rules[0]), int(_rules[1])))
            continue

        if COMMA in line:
            _pages = line.split(COMMA)
            pages.append([int(x) for x in _pages])

    return rules, pages


def _check_order_of_by(pages: Pages, rules: list[Rule]) -> bool:
    """Checks if given a batch of pages to be printed, it adheres to every rule."""
    is_order_correct = True
    for rule in rules:
        page_to_print = rule[0]
        page_to_follow = rule[1]
        if page_to_print not in pages:
            continue

        page_to_print_index = pages.index(page_to_print)
        pages_printed_before = pages[0:page_to_print_index]
        if page_to_follow in pages_printed_before:
            is_order_correct = False
            break

    return is_order_correct


def _find_middle_page(pages: Pages) -> Page:
    """Returns the middle page."""
    number_of_pages = len(pages)
    is_even = number_of_pages % 2 == 0
    if is_even:
        raise ValueError(f"Pages {pages} are even!")

    return pages[number_of_pages // 2]


def _calculate_sum_of_middlepages(batches: list[Pages], rules: list[Rule]) -> int:
    """Calculates the sum of the middle pages for each correct pages batch."""
    _sum = 0
    for batch in batches:
        is_correct_order = _check_order_of_by(batch, rules)
        if not is_correct_order:
            continue

        _sum += _find_middle_page(batch)

    return _sum


if __name__ == "__main__":
    main()
