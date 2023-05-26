import os
from dataclasses import dataclass

import utils

DAY = os.path.basename(__file__).split(".")[0]


@dataclass
class SectionInterval:
    start: int
    end: int


def find_sections_ranges(raw_sections: str) -> tuple[SectionInterval, SectionInterval]:
    """From the raw data, provides a tuple with the section interval for both elves."""
    first_range, second_range = raw_sections.split(",")
    start, end = first_range.split("-")
    first_section = SectionInterval(int(start), int(end))
    start, end = second_range.split("-")
    second_section = SectionInterval(int(start), int(end))

    return (first_section, second_section)


def find_complete_overlapping(
    section_1: SectionInterval, section_2: SectionInterval
) -> bool:
    """Find if two section are completely overlapped."""

    s1_overlap = section_1.start <= section_2.start and section_1.end >= section_2.end
    s2_overlap = section_2.start <= section_1.start and section_2.end >= section_1.end

    return s1_overlap or s2_overlap


def find_partial_overlapping(
    section_1: SectionInterval, section_2: SectionInterval
) -> bool:
    """Find if two section are partially overlapped."""

    s1_overlap = section_1.start <= section_2.start and section_1.end >= section_2.start
    s2_overlap = section_2.start <= section_1.start and section_2.end >= section_1.start

    return s1_overlap or s2_overlap


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    data = utils.load_input_data(DAY, debug)
    logger = utils.setup_logger(utils.create_log_level(debug))

    overlapped_couples = 0
    for elf_couple in data:
        s1, s2 = find_sections_ranges(elf_couple)
        is_overlapped = find_complete_overlapping(s1, s2)
        if is_overlapped:
            overlapped_couples += 1
            logger.debug(f"{s1=}, {s2=}")

    logger.info(
        f"First question answer. Complete overlapped sections are: {overlapped_couples}"
    )


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    data = utils.load_input_data(DAY, debug)
    logger = utils.setup_logger(utils.create_log_level(debug))

    overlapped_couples = 0
    for elf_couple in data:
        s1, s2 = find_sections_ranges(elf_couple)
        is_overlapped = find_partial_overlapping(s1, s2)
        if is_overlapped:
            overlapped_couples += 1
            logger.debug(f"{s1=}, {s2=}")

    logger.info(
        f"Second question answer. Partially overlapped sections are: {overlapped_couples}"
    )


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
