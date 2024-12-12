import os

import utils

DAY = os.path.basename(__file__).split(".")[0]
FILENAME = "03_first"
logger = utils.setup_logger(utils.create_log_level(False))

# an Input is equiavlent to the input file, read as a Matrix NxM
Input = list[list[str]]
# a batch is a list of N letters (4 by default)
Batch = list[str]


def first_question() -> None:
    """Function to solve the first question."""
    print("First question answer. ")


def second_question() -> None:
    """Function to solve the second question."""
    print("Second question answer. ")


def main() -> None:
    first_question()
    second_question()


def _build_data_from(filename: str) -> list[list[str]]:
    """Search on the input file for only the mul(x,y) strings."""
    data = utils.load_input_data(filename)
    return [list(x) for x in data]


def _extract_row_from(line: list[str], width: int = 4) -> list[Batch]:
    """Given a string, extract all the possible `width` lenght words."""
    possible_xmas: list[Batch] = list()
    i = 0
    while i < len(line) - width + 1:
        possible_xmas.append(line[i : i + width])
        i += 1

    return possible_xmas


def _check_for_xmas_from(batch: Batch) -> bool:
    """Given a batch, check if it's a XMAS batch (also reverse)."""
    XMAS = ["X", "M", "A", "S"]
    return XMAS == batch or XMAS == batch[::-1]


def _extract_horizontal_batch_from(report: Input) -> list[Batch]:
    """From the input extract horizontally every batch."""
    batches: list[Batch] = list()
    for line in report:
        batches.extend(_extract_row_from(line))

    return batches


def _extract_vertical_batch_from(report: Input) -> list[Batch]:
    """From the input extract vertically every batch."""
    batches: list[Batch] = list()

    columns = report[0]
    for index, _ in enumerate(columns):
        column: list[str] = list()
        for line in report:
            column.append(line[index])

        batches.extend(_extract_row_from(column))

    return batches


def _extract_diagonally_from_left_to_right_from(
    report: Input, width: int = 4
) -> list[Batch]:
    """From the input extract diagonnaly left->right every batch."""
    batches: list[Batch] = list()

    columns = report[0]
    rows = [line[0] for line in report]

    ROW_WIDTH = len(rows)
    COL_WIDTH = len(columns)
    logger.info(f"Matrix is: {ROW_WIDTH} rows X {COL_WIDTH} cols")

    starting_col = 0
    starting_row = 0
    MAX_BATCHES = (ROW_WIDTH - width + 1) + (COL_WIDTH - width + 1) - 1

    while len(batches) < MAX_BATCHES:
        batch: list[str] = list()
        temp_col = starting_col
        temp_row = starting_row
        logger.info(f"{starting_row=}, {starting_col=}")

        while temp_row < ROW_WIDTH and temp_col < COL_WIDTH:
            logger.info(f"{temp_row=} {temp_col=}")
            cell_value = report[temp_row][temp_col]
            logger.info(f"Adding {cell_value}")
            batch.append(cell_value)
            temp_row += 1
            temp_col += 1

        batches.append(batch)

        logger.info(
            f"At the end {starting_col=} {starting_row=}, batches {len(batches)}"
        )
        if starting_col < COL_WIDTH - width:
            starting_col += 1
        else:
            starting_col = 0
            starting_row += 1

    returned_batches: list[Batch] = list()
    for batch in batches:
        returned_batches.extend(_extract_row_from(batch))

    return returned_batches


def _revert(report: Input) -> Input:
    """Revert input (mirror it)."""
    new_report: Input = list()
    for row in report:
        new_report.append(row[::-1])

    return new_report


def _extract_diagonally_from_right_to_left_from(
    report: Input, width: int = 4
) -> list[Batch]:
    """From the input extract diagonnaly right->left every batch."""
    new_report = _revert(report)
    return _extract_diagonally_from_left_to_right_from(new_report)


def _count_xmas_from(filename: str) -> int:
    """Count the word XMAS in a given filename."""
    data = _build_data_from(filename)
    left_to_right = right_to_left = horizontally = vertically = 0

    for batch in _extract_diagonally_from_left_to_right_from(data):
        if _check_for_xmas_from(batch):
            left_to_right += 1
    for batch in _extract_diagonally_from_right_to_left_from(data):
        print(batch)
        if _check_for_xmas_from(batch):
            right_to_left += 1
    for batch in _extract_horizontal_batch_from(data):
        if _check_for_xmas_from(batch):
            horizontally += 1
    for batch in _extract_vertical_batch_from(data):
        if _check_for_xmas_from(batch):
            vertically += 1

    logger.info(f"{left_to_right=} {right_to_left=} {horizontally=} {vertically=}")
    return left_to_right + right_to_left + horizontally + vertically


if __name__ == "__main__":
    main()
