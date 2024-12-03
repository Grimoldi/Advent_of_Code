import os
from copy import deepcopy

import utils

DAY = os.path.basename(__file__).split(".")[0]
FILENAME = "02_first"
logger = utils.setup_logger(utils.create_log_level(False))

"""
A report is a list of levels (digits).
From the input file it a single line.
"""
Level = int
Report = list[Level]
Reports = list[Report]


def first_question() -> None:
    """Function to solve the first question."""
    reports = _build_data(FILENAME)
    print(
        "First question answer. "
        f"The number of correct report is: {_find_how_many_correct(reports)}"
    )


def second_question() -> None:
    """Function to solve the second question."""
    reports = _build_data(FILENAME)
    print(
        "Second question answer. "
        f"The number of correct report is: {_find_how_many_correct_with_dampener(reports)}"
    )


def _build_data(filename: str) -> Reports:
    """From the input file, build the data to work with."""
    raw_data = utils.load_input_data(filename)
    reports: Reports = list()
    for _report in raw_data:
        report: Report = list()
        levels = _report.split()
        for level in levels:
            report.append(int(level))

        reports.append(report)

    return reports


def _correct_order_of(report: Report) -> bool:
    """Checks that a report is always increasing or decreasing."""
    correct_order = report == sorted(report) or report == sorted(report, reverse=True)
    no_duplicates = len(set(report)) == len(report)
    return correct_order and no_duplicates


def _correct_range_of(report: Report, threshold: int = 3) -> bool:
    """Checks that all levels are within a threshold difference."""
    correct = True
    for index, level in enumerate(report):
        if index == 0:
            continue
        diff = abs(level - report[index - 1])
        if diff > threshold:
            correct = False
            break
    return correct


def _find_how_many_correct(reports: Reports) -> int:
    """Returns the number of correct report in the reports."""
    count = 0
    for report in reports:
        check_order = _correct_order_of(report)
        check_range = _correct_range_of(report)
        if not (check_order and check_range):
            continue

        count += 1
    return count


def _find_how_many_correct_with_dampener(reports: Reports) -> int:
    """Returns the number of correct report in the reports with the problem dampener."""
    count = 0
    for index, report in enumerate(reports):
        logger.info(f"Considering report #{index}.")
        check_order = _correct_order_of(report)
        check_range = _correct_range_of(report)

        if not (check_order and check_range):
            length = len(report)
            i = 0
            while i < length:
                logger.info(f"Started loop on report #{index} index {i}")
                new_report = deepcopy(report)
                removed = new_report.pop(i)
                logger.info(f"Removed {removed}, new report: {[x for x in new_report]}")
                check_order = _correct_order_of(new_report)
                check_range = _correct_range_of(new_report)

                if check_order and check_range:
                    break
                i += 1

        if not (check_order and check_range):
            logger.info(f"Report #{index} is UNSAFE.")
            logger.info(f"Report #{index} is {[x for x in report]}")
            continue

        logger.info(f"Report #{index} is SAFE.")
        count += 1
    return count


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()

# > 391
# < 422
