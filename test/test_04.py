import pytest

import day_04
from utils import load_input_data


@pytest.fixture
def _test_file() -> list[str]:
    """Loads the test file."""
    return load_input_data("04_test")


def test_cleaning_card_number(_test_file) -> None:
    """Test that the card number is removed from a line."""
    actual_line = day_04._clean_card_number(_test_file[5])
    expected_line = "31 18 13 56 72 | 74 77 10 23 35 67 36 11"
    assert actual_line == expected_line


def test_conversion_from_string_to_int() -> None:
    """Test that the conversion from raw strings to list of integers works."""
    line = "31 18 13 56 72 | 74 77 10 23 35 67 36 11"
    actual_winning, actual_hand = day_04._get_numbers(line)
    expected_winning = [31, 18, 13, 56, 72]
    expected_hand = [74, 77, 10, 23, 35, 67, 36, 11]

    assert actual_winning == expected_winning
    assert actual_hand == expected_hand


def test_winning_numbers_in_hand() -> None:
    """Test the match between the two list."""
    winning = [41, 48, 83, 86, 17]
    hand = [83, 86, 6, 31, 17, 9, 48, 53]

    actual_winning_hand = day_04._get_winning_numbers_in_hand(winning, hand)
    expected_winning_hand = [48, 83, 17, 86]

    assert sorted(actual_winning_hand) == sorted(expected_winning_hand)


def test_winning_points() -> None:
    """Test the calculation for winning cards in hand."""
    winning_hand = [48, 83, 17, 86]
    expected_points = 8
    actual_points = day_04._get_winning_point(winning_hand)

    assert actual_points == expected_points


def test_winning_points_for_empty_hand() -> None:
    """Test the calculation for winning cards in hand if no winning card is in hand."""
    winning_hand = []
    expected_points = 0
    actual_points = day_04._get_winning_point(winning_hand)

    assert actual_points == expected_points


def test_first_question(_test_file) -> None:
    """Test the first question."""
    data = _test_file

    actual_points = 0
    for raw_line in data:
        card = day_04._clean_card_number(raw_line)
        winning, hand = day_04._get_numbers(card)
        winning_in_hand = day_04._get_winning_numbers_in_hand(winning, hand)
        actual_points += day_04._get_winning_point(winning_in_hand)

    expected_points = 13
    assert expected_points == actual_points


def test_scratchcards_copies() -> None:
    """Test scratchcardsCopies class."""
    scratch_cards = day_04.ScratchCardsCopies()
    scratch_cards.add_copy(1)
    scratch_cards.add_copy(1)
    scratch_cards.add_copy(3)

    assert 3 == scratch_cards.get_copies(1)
    assert 1 == scratch_cards.get_copies(2)
    assert 2 == scratch_cards.get_copies(3)


def test_adding_of_scratchcards(_test_file) -> None:
    """Test adding scratchards based on winning."""
    scratch_cards = day_04.ScratchCardsCopies()
    day_04.add_copies(1, 2, scratch_cards)

    assert scratch_cards.get_copies(1) == 1
    assert scratch_cards.get_copies(2) == 2
    assert scratch_cards.get_copies(3) == 2
    assert scratch_cards.get_copies(4) == 1

    day_04.add_copies(2, 1, scratch_cards)
    assert scratch_cards.get_copies(3) == 4


def test_second_question(_test_file) -> None:
    """Test the second question."""
    data = _test_file
    print()

    scratch_cards = day_04.ScratchCardsCopies()
    actual_points = 0

    for raw_line in data:
        card_number = day_04._get_card_number(raw_line)
        card = day_04._clean_card_number(raw_line)
        winning, hand = day_04._get_numbers(card)
        winning_in_hand = day_04._get_winning_numbers_in_hand(winning, hand)

        cards_won = len(winning_in_hand)
        # won_copies = cards_won * scratch_cards.get_copies(card_number)

        day_04.add_copies(
            card_number,
            cards_won,
            scratch_cards,
        )
        actual_points += scratch_cards.get_copies(card_number)

    expected_points = 30
    assert expected_points == actual_points
