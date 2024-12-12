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
    rules, pages = _build_data_from(FILENAME)
    rules = _sort_rules(rules)
    print(
        "Second question answer. "
        f"The total sum is: {_calculate_sum_of_incorrect_middlepages(pages, rules)}"
    )


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
        is_correct_order = _check_order_of_by_single(pages, rule)
        if not is_correct_order:
            is_order_correct = False
            break

    return is_order_correct


def _check_order_of_by_single(pages: Pages, rule: Rule) -> bool:
    """Checks given pages by a single rule."""
    page_to_print, page_to_follow = rule
    if page_to_print not in pages:
        return True

    page_to_print_index = pages.index(page_to_print)
    pages_printed_before = pages[0:page_to_print_index]

    return page_to_follow not in pages_printed_before


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


def _sort_rules(rules: list[Rule]) -> list[Rule]:
    """
    Sort the rules.
    The first page take precedence.
    In case of a tie, the latter page takes precedence.
    """
    return sorted(rules, key=lambda tup: (tup[0], tup[1]))


def _resort_by_single(pages: Pages, rule: Rule) -> None:
    """
    Resort the pages in order to adhere to the rule.
    The page in the wrong order has to be moved before the page second to be printed.
    """
    first_page, second_page = rule
    index_first = pages.index(first_page)
    index_second = pages.index(second_page)
    pages.pop(index_first)
    pages.insert(index_second, first_page)


def _calculate_sum_of_incorrect_middlepages(
    batches: list[Pages], rules: list[Rule]
) -> int:
    """Calculates the sum of the middle pages for each incorrect pages batch."""
    _sum = 0
    for pages in batches:
        correct_order = True
        for rule in rules:
            is_correct_order = _check_order_of_by_single(pages, rule)
            if is_correct_order:
                continue

            _resort_by_single(pages, rule)
            correct_order = False

        # sum only if at least a rule was not strictly followed
        if not correct_order:
            _sum += _find_middle_page(pages)

    return _sum


if __name__ == "__main__":
    main()

# < 4581
