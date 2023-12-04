from dataclasses import dataclass

from utils import load_input_data


@dataclass(frozen=True)
class EngineNumber:
    row: int
    col: int
    number: int
    power_of_ten: int


@dataclass
class EngineSymbol:
    row: int
    col: int
    symbol: str


def parse_engine_line_for_raw(
    line: str, row: int
) -> tuple[list[EngineNumber], list[EngineSymbol]]:
    """Gets the number and their position from raw."""

    def _build_engine_number() -> EngineNumber:
        """Build an Engine Number."""
        return EngineNumber(row, starting_col, number, _get_power_of_ten(digits))

    def _build_engine_symbol() -> EngineSymbol:
        """Build an Engine Symbol."""
        return EngineSymbol(row, col, symbol)

    FULLSTOP = "."
    UNMATCHED_COL = -1
    starting_col = UNMATCHED_COL
    engine_numbers: list[EngineNumber] = list()
    engine_symbols: list[EngineSymbol] = list()
    digits: list[int] = list()

    max_col = len(line) - 1

    for col, char in enumerate(line):
        if char == FULLSTOP:
            if len(digits) > 0:
                number = _get_value_from_list_of_digits(digits)
                engine_numbers.append(_build_engine_number())
                digits: list[int] = list()

            starting_col = UNMATCHED_COL
            continue

        try:
            digit = int(char)
            digits.append(digit)
            if starting_col == UNMATCHED_COL:
                starting_col = col

        except ValueError as _:
            if len(digits) > 0:
                number = _get_value_from_list_of_digits(digits)
                engine_numbers.append(_build_engine_number())
                digits: list[int] = list()
                starting_col = UNMATCHED_COL

            symbol = char
            engine_symbols.append(_build_engine_symbol())

        if col == max_col:
            if len(digits) > 0:
                number = _get_value_from_list_of_digits(digits)
                engine_numbers.append(_build_engine_number())
                digits: list[int] = list()

    return (engine_numbers, engine_symbols)


def _get_power_of_ten(digits: list[int]) -> int:
    """Gets the power of ten from a list of digits."""
    return len(digits) - 1


def _get_value_from_list_of_digits(digits: list[int]) -> int:
    """Gets the numeric value from a list of digits ([1,2,3] -> 123)"""
    ten_power = _get_power_of_ten(digits)
    number = 0
    for index, digit in enumerate(digits):
        number += digit * 10 ** (ten_power - index)

    return number


def _filter_part_numbers(
    symbols: list[EngineSymbol], numbers: list[EngineNumber], max_length: int
) -> list[EngineNumber]:
    """Filters the Part Numbers (those close to a symbol)."""
    part_numbers: list[EngineNumber] = list()
    for symbol in symbols:
        for number in numbers:
            # skip if there are more than a single row between them.
            if abs(number.row - symbol.row) > 1:
                continue

            # skip if there are more than a colum betweend them on a different row
            left_range = max(0, number.col - 1)
            right_range = min(number.col + number.power_of_ten + 1, max_length)
            if not left_range <= symbol.col <= right_range:
                continue

            part_numbers.append(number)

    return part_numbers


EngineGear = tuple[EngineNumber, EngineNumber]


def _get_gears(
    symbols: list[EngineSymbol], numbers: list[EngineNumber], max_length: int
) -> list[EngineGear]:
    """Gets the gears. A gear are two number close to the same * symbol."""
    gears: list[EngineGear] = list()
    GEAR_SYMBOL = "*"
    for symbol in symbols:
        maybe_gears: list[EngineNumber] = list()

        if symbol.symbol != GEAR_SYMBOL:
            continue

        for number in numbers:
            # skip if there are more than a single row between them.
            if abs(number.row - symbol.row) > 1:
                continue

            # skip if there are more than a colum betweend them on a different row
            left_range = max(0, number.col - 1)
            right_range = min(number.col + number.power_of_ten + 1, max_length)
            if not left_range <= symbol.col <= right_range:
                continue
            maybe_gears.append(number)

        if len(maybe_gears) == 2:
            gears.append((maybe_gears[0], maybe_gears[1]))

    return gears


def main():
    first_question()
    second_question()


def first_question() -> None:
    """Answers to the first question."""
    data = load_input_data("03_input")
    line_length = len(data[0])

    symbols: list[EngineSymbol] = list()
    numbers: list[EngineNumber] = list()
    for row, line in enumerate(data):
        num, sym = parse_engine_line_for_raw(line, row)
        numbers.extend(num)
        symbols.extend(sym)

    filterd_numbers = _filter_part_numbers(symbols, numbers, line_length)
    print(
        f"Len of numbers: {len(numbers)}, len of filtered numbers: {len(filterd_numbers)}"
    )

    print(f"Part number sum is {sum(x.number for x in filterd_numbers)}.")


def second_question() -> None:
    """Answers to the second question."""
    data = load_input_data("03_input")
    line_length = len(data[0])

    symbols: list[EngineSymbol] = list()
    numbers: list[EngineNumber] = list()

    for row, line in enumerate(data):
        num, sym = parse_engine_line_for_raw(line, row)
        numbers.extend(num)
        symbols.extend(sym)

    gears = _get_gears(symbols, numbers, line_length)
    gear_ratios = [x[0].number * x[1].number for x in gears]

    print(f"The sum of all gear ratio is: {sum(gear_ratios)}.")


if __name__ == "__main__":
    main()
