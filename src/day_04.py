import re
from dataclasses import dataclass

from utils import load_input_data


@dataclass
class ScratchCardsCopies:
    def __post_init__(self) -> None:
        """Creates the internal structure for keeping track of the Scratchcards copies."""
        self._cards: dict[int, int] = dict()

    def add_copy(self, card: int, copies: int = 1) -> None:
        """Adds copies of a card."""
        try:
            self._cards[card] += copies
        except KeyError:
            self._cards[card] = copies
        # print(f"Added {copies} copy of card {card}.")

    def get_copies(self, card: int) -> int:
        """
        Gets the amount of copies for a given card.
        Note that every card is at least one copy (the original one).
        """
        return self._cards.get(card, 0) + 1


def main():
    first_question()
    second_question()


def first_question() -> None:
    """Answers to the first question."""
    data = load_input_data("04_input")

    winning_points = 0
    for raw_line in data:
        card = _clean_card_number(raw_line)
        winning, hand = _get_numbers(card)
        winning_in_hand = _get_winning_numbers_in_hand(winning, hand)
        winning_points += _get_winning_point(winning_in_hand)

    print(f"Total winning points are: {winning_points}")


def second_question() -> None:
    """Answers to the second question."""
    data = load_input_data("04_input")

    scratch_cards = ScratchCardsCopies()
    winning_points = 0

    for raw_line in data:
        card_number = _get_card_number(raw_line)
        card = _clean_card_number(raw_line)
        winning, hand = _get_numbers(card)
        winning_in_hand = _get_winning_numbers_in_hand(winning, hand)

        cards_won = len(winning_in_hand)
        # won_copies = cards_won * scratch_cards.get_copies(card_number)

        add_copies(
            card_number,
            cards_won,
            scratch_cards,
        )
        winning_points += scratch_cards.get_copies(card_number)

    print(f"Total winning points are: {winning_points}")


WinningNumbers = list[int]
HandNumbers = list[int]


def _clean_card_number(raw_line: str) -> str:
    """Clean the line from the initial card number."""
    return re.sub(r"Card\s+\d+\:\s", "", raw_line)


def _get_card_number(raw_line: str) -> int:
    """Gets a card number from a given string line."""
    pattern = re.compile(r"Card\s+(?P<card_id>\d+)\:")
    regex_group = pattern.search(raw_line)

    if regex_group is None:
        raise ValueError(f"Unable to find Card id in line {raw_line}")

    return int(regex_group.group("card_id"))


def add_copies(
    starting_card: int, number_of_cards: int, card_copies: ScratchCardsCopies
) -> None:
    """Add a copy starting from a given card for the number of specified cards."""
    card_index = starting_card + 1
    last_card = card_index + number_of_cards
    number_of_copies_won = card_copies.get_copies(starting_card)

    while card_index < last_card:
        card_copies.add_copy(card_index, number_of_copies_won)
        card_index += 1


def _get_numbers(raw_line: str) -> tuple[WinningNumbers, HandNumbers]:
    """From a line, gets the winning numbers and the numbers in hand."""
    winning, hand = raw_line.split("|")
    winning_numbers = _load_numbers(winning.split())
    hand_numbers = _load_numbers(hand.split())

    return winning_numbers, hand_numbers


def _load_numbers(raw_numbers: list[str]) -> list[int]:
    """Converts string numbers to int numbers."""
    return [int(x) for x in raw_numbers]


def _get_winning_numbers_in_hand(winnings: list[int], hands: list[int]) -> list[int]:
    """Gets the winning numbers in hand."""
    return list(set(hands) & set(winnings))


def _get_winning_point(winning_hand: list[int]) -> int:
    """Gets the point from the winning cards in hand."""
    return int(2 ** (len(winning_hand) - 1))


def _count_won_scratchcards(winning_hand: list[int]) -> int:
    """Gets how many scratchcard won from a single scratchcard."""
    return len(winning_hand)


if __name__ == "__main__":
    main()
