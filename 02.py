import os
from enum import Enum, auto

import utils

DAY = os.path.basename(__file__).split(".")[0]


class RPS(Enum):
    """Enumeration for signs."""

    ROCK = auto()
    SCISSORS = auto()
    PAPER = auto()


class Output(Enum):
    """Enumeration for results."""

    WIN = auto()
    DRAW = auto()
    LOSE = auto()


def find_result(own: RPS, opponent: RPS) -> Output:
    """Given two signs, find the result."""
    winning_combo = [
        (RPS.SCISSORS, RPS.PAPER),
        (RPS.PAPER, RPS.ROCK),
        (RPS.ROCK, RPS.SCISSORS),
    ]

    if own.value == opponent.value:
        return Output.DRAW

    round_try = (own, opponent)
    if round_try in winning_combo:
        return Output.WIN

    else:
        return Output.LOSE


def find_sign_from_result(result: Output, opponent: RPS) -> RPS:
    """Given the opposite sign and the result, find what sign I should play."""
    winning_combo = {
        RPS.PAPER: RPS.SCISSORS,
        RPS.ROCK: RPS.PAPER,
        RPS.SCISSORS: RPS.ROCK,
    }
    losing_combo = {
        RPS.PAPER: RPS.ROCK,
        RPS.ROCK: RPS.SCISSORS,
        RPS.SCISSORS: RPS.PAPER,
    }

    if result == Output.DRAW:
        return opponent
    elif result == Output.WIN:
        return winning_combo[opponent]
    elif result == Output.LOSE:
        return losing_combo[opponent]
    else:
        raise ValueError(f"Unable to recognize the Output value ({result})!")


def calculate_sign_score(sign: RPS) -> int:
    """Given the sign played, find the score."""
    mapping = {RPS.ROCK: 1, RPS.PAPER: 2, RPS.SCISSORS: 3}
    return mapping[sign]


def calculate_output_score(output: Output) -> int:
    """Given the round output, find the score."""
    mapping = {
        Output.LOSE: 0,
        Output.DRAW: 3,
        Output.WIN: 6,
    }

    return mapping[output]


def convert_sign(raw: str) -> RPS:
    """Given a raw sign, convert to an RPS instance."""
    mapping = {
        "X": RPS.ROCK,
        "Y": RPS.PAPER,
        "Z": RPS.SCISSORS,
        "A": RPS.ROCK,
        "B": RPS.PAPER,
        "C": RPS.SCISSORS,
    }

    return mapping[raw]


def convert_result(raw: str) -> Output:
    """Given a raw result, convert to an Output instance."""
    mapping = {"X": Output.LOSE, "Y": Output.DRAW, "Z": Output.WIN}

    return mapping[raw]


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    matches = utils.load_input_data(DAY, debug)
    logger = utils.setup_logger(utils.create_log_level(debug))

    total_score = 0
    for match in matches:

        bets = match.split(" ")
        opponent = convert_sign(bets[0])
        own = convert_sign(bets[1])

        result = find_result(own, opponent)
        match_score = calculate_output_score(result)
        sign_score = calculate_sign_score(own)

        final_score = match_score + sign_score
        total_score += final_score

        logger.debug(f"{bets=}, {result=}, {opponent=}, {own=}")
        logger.debug(f"{match_score=}, {sign_score=}")

    logger.info(f"Total score for first strategy: {total_score}")


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    matches = utils.load_input_data(DAY, debug)
    logger = utils.setup_logger(utils.create_log_level(debug))

    total_score = 0
    for match in matches:

        bets = match.split(" ")
        opponent = convert_sign(bets[0])
        result = convert_result(bets[1])
        own = find_sign_from_result(result, opponent)

        match_score = calculate_output_score(result)
        sign_score = calculate_sign_score(own)

        final_score = match_score + sign_score
        total_score += final_score

        logger.debug(f"{bets=}, {result=}, {opponent=}, {own=}")
        logger.debug(f"{match_score=}, {sign_score=}")

    logger.info(f"Total score for second strategy: {total_score}")


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
