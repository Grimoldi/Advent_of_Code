import re
from dataclasses import dataclass
from enum import StrEnum, auto

from utils import load_input_data


class Dice(StrEnum):
    BLUE = auto()
    RED = auto()
    GREEN = auto()


@dataclass
class SingleRound:
    greens: int
    reds: int
    blues: int


@dataclass
class Game:
    game_id: int
    rounds: list[SingleRound]
    max_reds: int = 12
    max_greens: int = 13
    max_blues: int = 14

    @property
    def is_valid(self) -> bool:
        """Checks if the game respects its limits."""
        is_valid = True
        for single_round in self.rounds:
            if (
                single_round.blues > self.max_blues
                or single_round.greens > self.max_greens
                or single_round.reds > self.max_reds
            ):
                is_valid = False
                break

        return is_valid

    @property
    def min_blues_for_valid_game(self) -> int:
        """Returns the minimum number of blue dices for the game to be valid."""
        return max([x.blues for x in self.rounds])

    @property
    def min_greens_for_valid_game(self) -> int:
        """Returns the minimum number of green dices for the game to be valid."""
        return max([x.greens for x in self.rounds])

    @property
    def min_reds_for_valid_game(self) -> int:
        """Returns the minimum number of red dices for the game to be valid."""
        return max([x.reds for x in self.rounds])

    @property
    def power(self) -> int:
        """Returns the power of the game."""
        return (
            self.min_reds_for_valid_game
            * self.min_blues_for_valid_game
            * self.min_greens_for_valid_game
        )


def parse_game(game: str) -> Game:
    """Parse a game from raw data"""
    game_id = get_game_id(game)
    rounds_line = re.sub(r"Game \d+\: ", "", game)
    game_rounds = rounds_line.split(";")
    round_dices: list[SingleRound] = list()
    for game_round in game_rounds:
        single_round = get_dices_from_single_round(game_round)
        round_dices.append(single_round)

    return Game(game_id, round_dices)


def get_game_id(line: str) -> int:
    """Get the raw game id."""
    game_compiler = re.compile(r"Game (?P<game_id>\d+)\:")
    regex_group = game_compiler.search(line)
    if regex_group is None:
        raise ValueError(f"Unable to find Game id in line {line}")

    return int(regex_group.group("game_id"))


def get_dices_from_single_round(game_round: str) -> SingleRound:
    """From a string round get the SingleRound object."""
    blues_compiler = get_blue_dice_compiler()
    blues_group = blues_compiler.search(game_round)
    blues = get_dice_from_regex(blues_group, Dice.BLUE)

    greens_compiler = get_green_dice_compiler()
    greens_group = greens_compiler.search(game_round)
    greens = get_dice_from_regex(greens_group, Dice.GREEN)

    reds_compiler = get_red_dice_compiler()
    reds_group = reds_compiler.search(game_round)
    reds = get_dice_from_regex(reds_group, Dice.RED)

    return SingleRound(greens=greens, reds=reds, blues=blues)


def get_blue_dice_compiler() -> re.Pattern[str]:
    """Gets the pattern for the blue dices."""
    return re.compile(r"(.*\, )?(?P<blues>\d+ blue).*$")


def get_red_dice_compiler() -> re.Pattern[str]:
    """Gets the pattern for the red dices."""
    return re.compile(r"(.*\, )?(?P<reds>\d+ red).*$")


def get_green_dice_compiler() -> re.Pattern[str]:
    """Gets the pattern for the green dices."""
    return re.compile(r"(.*\, )?(?P<greens>\d+ green).*$")


def get_dice_from_regex(matched: re.Match | None, color: Dice) -> int:
    """Gets the number of dice from the regex."""
    if matched is None:
        return 0

    matched_group = matched.group(f"{color.value}s")
    if matched_group is None:
        return 0

    return int(matched_group.replace(color.value, "").strip())


def main():
    first_question()
    second_question()


def first_question() -> None:
    """Answers to the first question."""
    data = load_input_data("02_input")
    games: list[Game] = list()
    for game in data:
        games.append(parse_game(game))

    valid_games = [x for x in games if x.is_valid]
    print(f"Valid games ID sum is: {sum(x.game_id for x in valid_games)}")


def second_question() -> None:
    """Answers to the second question."""
    data = load_input_data("02_input")
    games: list[Game] = list()
    for game in data:
        games.append(parse_game(game))

    print(f"Total games power is: {sum(x.power for x in games)}")


if __name__ == "__main__":
    main()
