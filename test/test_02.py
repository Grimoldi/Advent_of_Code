import re

import day_02
from utils import load_input_data


def test_game_id() -> None:
    """Test that given a list of single digits integers, the double digit number is what's expected."""
    data = load_input_data("02_test")
    game_id = day_02.get_game_id(data[3])
    assert game_id == 4


def test_regex_for_round() -> None:
    """Test that the group regex is working as expected."""
    test_round = "3 green, 4 red"

    blues_compiler = day_02.get_blue_dice_compiler()
    blues_group = blues_compiler.search(test_round)
    blues = day_02.get_dice_from_regex(blues_group, day_02.Dice.BLUE)
    assert blues == 0

    greens_compiler = day_02.get_green_dice_compiler()
    greens_group = greens_compiler.search(test_round)
    greens = day_02.get_dice_from_regex(greens_group, day_02.Dice.GREEN)
    assert greens == 3

    reds_compiler = day_02.get_red_dice_compiler()
    reds_group = reds_compiler.search(test_round)
    reds = day_02.get_dice_from_regex(reds_group, day_02.Dice.RED)
    assert reds == 4


def test_singleround_from_raw() -> None:
    """Test the parsing of a single round."""
    test_rounds = ["3 blue, 4 red", "1 red, 2 green, 6 blue", "2 green"]
    expected_single_rounds = [
        day_02.SingleRound(greens=0, reds=4, blues=3),
        day_02.SingleRound(greens=2, reds=1, blues=6),
        day_02.SingleRound(greens=2, reds=0, blues=0),
    ]
    for index, test_round in enumerate(test_rounds):
        actual_round = day_02.get_dices_from_single_round(test_round)
        assert actual_round == expected_single_rounds[index]


def test_game() -> None:
    """Test the parsing of a single game."""
    test_game = "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    rounds = [
        day_02.SingleRound(reds=6, blues=1, greens=3),
        day_02.SingleRound(reds=1, blues=2, greens=2),
    ]
    expected_game = day_02.Game(game_id=5, rounds=rounds)
    game = day_02.parse_game(test_game)

    assert game == expected_game


def test_valid_game() -> None:
    """Test if a valid game."""
    test_game = "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    game = day_02.parse_game(test_game)

    assert game.is_valid == True


def test_invalid_game() -> None:
    """Test an invalid game."""
    test_game = (
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
    )
    game = day_02.parse_game(test_game)

    assert game.is_valid == False


def test_first_question() -> None:
    """Test first question."""

    data = load_input_data("02_test")
    games: list[day_02.Game] = list()
    for game in data:
        games.append(day_02.parse_game(game))

    valid_games = [x for x in games if x.is_valid]
    game_id_sum = sum(x.game_id for x in valid_games)
    assert game_id_sum == 8


def test_minimum_red_dices_for_valid_game() -> None:
    """Test the minimum number of red dice for a game to be valid."""
    test_game = (
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
    )
    game = day_02.parse_game(test_game)

    assert game.min_reds_for_valid_game == 20


def test_power_of_a_game() -> None:
    """Tests the power of a game."""
    test_game = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    game = day_02.parse_game(test_game)

    assert game.power == 48


def test_second_question() -> None:
    """Test second question."""
    data = load_input_data("02_test")
    games: list[day_02.Game] = list()
    for game in data:
        games.append(day_02.parse_game(game))

    game_power_sum = sum(x.power for x in games)
    assert game_power_sum == 2286
