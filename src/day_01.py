import os

import data_loader

DAY = os.path.basename(__file__).split(".")[0]
FILENAME = "01_first"


def first_question() -> None:
    """Function to solve the first question."""
    print(
        "First question answer. "
        f"The total distance is: {_find_total_distance(FILENAME)}"
    )


def second_question() -> None:
    """Function to solve the second question."""
    print(
        "Second question answer. "
        f"The total similarity score is: {_find_total_similarity_score(FILENAME)}"
    )


def _build_data(filename: str) -> tuple[list[int], list[int]]:
    """From the input file, build the data to work with."""
    raw_data = data_loader.load_input_data(filename)
    first_half: list[int] = list()
    second_half: list[int] = list()
    for line in raw_data:
        first_col, second_col = line.split()
        first_half.append(int(first_col))
        second_half.append(int(second_col))

    return (sorted(first_half), sorted(second_half))


def _find_total_distance(filename: str) -> int:
    """Given the raw data file, find the total distance."""
    left_col, right_col = _build_data(filename)
    distance_sum = 0
    for left_digit, right_digit in zip(left_col, right_col):
        distance_sum += abs(left_digit - right_digit)

    return distance_sum


def _find_total_similarity_score(filename: str) -> int:
    """Given the raw data file, find the total similarity."""
    left_col, right_col = _build_data(filename)
    similarity_score = 0
    for digit in left_col:
        occurrence = right_col.count(digit)
        similarity_score += digit * occurrence

    return similarity_score


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
