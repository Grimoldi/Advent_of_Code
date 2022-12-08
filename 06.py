import os

from utils import load_input_data

DAY = os.path.basename(__file__).split(".")[0]


def find_nonrepeated_index(signal: str, size: int):
    """Finds the first index of the not repeated subset of characters."""
    index = -1
    for index, _ in enumerate(signal):
        if index < size:
            continue

        subset = signal[index - size : index]
        if find_unique_values(subset, size):
            break
    return index


def find_unique_values(signal_subset: str, size: int) -> bool:
    """Find if in a particular subset there are reapeted values."""
    unique = True
    for char in signal_subset:
        new_subset = signal_subset.replace(char, "")
        if len(new_subset) != (size - 1):
            unique = False

    return unique


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    data = load_input_data(DAY, debug)
    SIZE = 4
    print(
        f"First question answer. The first non repeated index is: {find_nonrepeated_index(data[0], SIZE)}"
    )


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    data = load_input_data(DAY, debug)
    SIZE = 14
    print(
        f"Second question answer. The first non repeated index is: {find_nonrepeated_index(data[0], SIZE)}"
    )


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
