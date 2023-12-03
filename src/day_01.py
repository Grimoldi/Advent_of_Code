import os

from utils import load_input_data


def main():
    first_question()
    second_question()


def first_question() -> None:
    """Answers to the first question."""
    data = load_input_data("01_f_input")
    digits = find_double_digit_coordinate(data)
    print(f"{[x for x in digits]}\n{sum(digits)}")


def second_question() -> None:
    """Answers to the second question."""
    data = load_input_data("01_s_input")
    digits = find_double_digit_coordinate_even_from_string(data)
    print(f"{[x for x in digits]}\n{sum(digits)}")


def find_double_digit_coordinate(data: list[str]) -> list[int]:
    """From the raw data extract the double digits coordinates."""
    digits: list[int] = list()
    for line in data:
        numbers = list()
        for char in line:
            try:
                digit = int(char)
                numbers.append(digit)
            except ValueError as _:
                continue

        digits.append(get_digits_from_list(numbers))

    return digits


def find_double_digit_coordinate_even_from_string(data: list[str]) -> list[int]:
    """From the raw data extract the double digits coordinates. First ten numbers are also valid as strings."""

    def convert_name_to_number(name: str) -> int:
        """Convert the name to the number."""
        return MAPPING[name]

    def match_key_name(substring: str) -> bool:
        """Checks if a substring matches a key name."""
        matched = [x for x in MAPPING.keys() if x.startswith(substring)]
        return len(matched) > 0

    MAPPING = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    digits: list[int] = list()

    for line in data:
        numbers = list()
        for index, char in enumerate(line):
            try:
                digit = int(char)
                numbers.append(digit)
            except ValueError as _:
                i = 1
                substring = line[index : index + i]
                while match_key_name(substring) and i <= len(line):
                    i += 1
                    substring = line[index : index + i]
                word_number = line[index : index + i - 1]
                if word_number in MAPPING:
                    numbers.append(convert_name_to_number(word_number))

        digits.append(get_digits_from_list(numbers))

    return digits


def get_digits_from_list(numbers: list[int]) -> int:
    """Gets a double digits number from a list of int."""
    return 10 * numbers[0] + numbers[-1]


if __name__ == "__main__":
    main()
