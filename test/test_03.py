import day_03
from utils import load_input_data


def test_number_from_list() -> None:
    """Test that given a list of single digits integers, the numeric value is what's expected."""
    numbers = [1, 2, 3, 4]
    double_digits = day_03._get_value_from_list_of_digits(numbers)
    assert double_digits == 1234


def test_line_parsing() -> None:
    """Test how a line is parsed."""
    data = load_input_data("03_test")
    row = 5
    line = data[row - 1]
    numbers, symbols = day_03.parse_engine_line_for_raw(line, row)

    expected_numbers = [day_03.EngineNumber(row, 0, 617, 2)]
    expected_symbol = [day_03.EngineSymbol(row, 3, "*")]

    assert expected_numbers == numbers
    assert expected_symbol == symbols

    row = 10
    line = data[row - 1]
    numbers, symbols = day_03.parse_engine_line_for_raw(line, row)

    expected_numbers = [
        day_03.EngineNumber(row, 1, 664, 2),
        day_03.EngineNumber(row, 5, 598, 2),
    ]
    expected_symbol = []

    assert expected_numbers == numbers
    assert expected_symbol == symbols


def test_part_numbers_filtering() -> None:
    """Test if the part numbers are filtered correctly."""
    first_row_numbers = [
        day_03.EngineNumber(0, 0, 467, 2),
        day_03.EngineNumber(0, 5, 114, 2),
    ]
    first_row_symbols = []

    second_row_numbers = []
    second_row_symbols = [day_03.EngineSymbol(1, 3, "*")]

    third_row_numbers = [
        day_03.EngineNumber(2, 2, 35, 1),
        day_03.EngineNumber(2, 6, 633, 2),
    ]
    third_row_symbols = []

    forth_row_numbers = []
    forth_row_symbols = [day_03.EngineSymbol(3, 6, "#")]

    symbols = second_row_symbols + forth_row_symbols
    numbers = first_row_numbers + third_row_numbers

    expected_numbers = [
        day_03.EngineNumber(0, 0, 467, 2),
        day_03.EngineNumber(2, 2, 35, 1),
        day_03.EngineNumber(2, 6, 633, 2),
    ]
    filtered_parts = day_03._filter_part_numbers(symbols, numbers, 11)

    assert filtered_parts == expected_numbers


def test_first_question() -> None:
    """Test first question."""
    data = load_input_data("03_test")
    line_length = len(data[0])

    symbols: list[day_03.EngineSymbol] = list()
    numbers: list[day_03.EngineNumber] = list()

    for row, line in enumerate(data):
        num, sym = day_03.parse_engine_line_for_raw(line, row)
        numbers.extend(num)
        symbols.extend(sym)

    filterd_numbers = day_03._filter_part_numbers(symbols, numbers, line_length)
    expected_sum = 4_361
    actual_sum = sum(x.number for x in filterd_numbers)

    assert actual_sum == expected_sum


def test_gear_filtering() -> None:
    """Test if the gear filter works."""
    data = load_input_data("03_test")
    rows = [0, 1, 2]
    symbols: list[day_03.EngineSymbol] = list()
    numbers: list[day_03.EngineNumber] = list()

    for row in rows:
        line = data[row]
        num, sym = day_03.parse_engine_line_for_raw(line, row)
        numbers.extend(num)
        symbols.extend(sym)

    expected_gear = [
        (
            day_03.EngineNumber(0, 0, 467, 2),
            day_03.EngineNumber(2, 2, 35, 1),
        )
    ]
    actual_gear = day_03._get_gears(symbols, numbers, len(data[0]))

    assert expected_gear == actual_gear


def test_second_question() -> None:
    """Test second question."""
    data = load_input_data("03_test")
    line_length = len(data[0])

    symbols: list[day_03.EngineSymbol] = list()
    numbers: list[day_03.EngineNumber] = list()

    for row, line in enumerate(data):
        num, sym = day_03.parse_engine_line_for_raw(line, row)
        numbers.extend(num)
        symbols.extend(sym)

    gears = day_03._get_gears(symbols, numbers, line_length)
    gear_ratios = [x[0].number * x[1].number for x in gears]

    actual_sum = sum(gear_ratios)
    expected_sum = 467_835
    # print(f"\n{gear_ratios}")

    assert actual_sum == expected_sum
