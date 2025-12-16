import data_loader
import day_01

EXAMPLE = "01_test"
REAL = "01_input"


def test_import_data(filename=EXAMPLE) -> None:
    """Test loading of file."""
    instructions = data_loader.load_input_data(filename)
    actual = instructions[0:2]
    expected = ["L68", "L30"]
    assert actual == expected


def test_first_question(filename=EXAMPLE) -> None:
    """Test the first question with example data."""
    instructions = data_loader.load_input_data(filename)
    actual = day_01._rotate_dial(instructions)
    expected = 3
    assert actual == expected


def test_first_question_real(filename=REAL) -> None:
    """Test the first question."""
    instructions = data_loader.load_input_data(filename)
    actual = day_01._rotate_dial(instructions)
    expected = 1168
    assert actual == expected


def test_second_question(filename=EXAMPLE) -> None:
    """Test the first question with example data."""
    instructions = data_loader.load_input_data(filename)
    actual = day_01._rotate_dial_secure_password(instructions)
    expected = 6
    assert actual == expected


def test_second_question_real(filename=REAL) -> None:
    """Test the first question with example data."""
    instructions = data_loader.load_input_data(filename)
    actual = day_01._rotate_dial_secure_password(instructions)
    expected = 7199
    assert actual == expected


def test_edge_case() -> None:
    """Test the edge case proposed in the second question."""
    actual_zeros, actual_end_dial = day_01._turn_rigt(50, 1000)
    expected_zeros = 10
    expected_end_dial = 50

    assert actual_zeros == expected_zeros
    assert actual_end_dial == expected_end_dial
