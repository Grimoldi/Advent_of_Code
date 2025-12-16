import sys
from typing import Any, Generator

from loguru import logger

import data_loader

FILENAME = "02_input"
LEVEL = "DEBUG"
LEVEL = "INFO"

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    level=LEVEL,
)


def first_question(filename=FILENAME) -> None:
    """Function to solve the first question."""
    print(f"Solution of the first question is: {_sum_invalid_ids(FILENAME)}")


def second_question(filename=FILENAME) -> None:
    """Function to solve the second question."""
    print(f"Solution of the first question is: {_sum_invalid_ids_chunks(FILENAME)}")


def _build_id_ranges(filename: str) -> Generator[tuple[int, int], Any, Any]:
    """Split data to id ranges."""
    data = data_loader.load_input_data(filename)[0]
    for line in data.split(","):
        yield int(line.split("-")[0]), int(line.split("-")[1])


def _sum_invalid_ids(filename: str) -> int:
    """Sum all the invalid ids within ranges."""
    gen = _build_id_ranges(filename)
    invalid_ids = []
    for bot, top in gen:
        invalid_ids.extend(_find_invalid_ids(bot, top))
    return sum(invalid_ids)


def _find_invalid_ids(bot_range: int, top_range: int) -> list[int]:
    """Get all the invalid ids in a range."""
    invalid_ids = []
    logger.debug(f"Checking between {bot_range} and {top_range}.")
    while bot_range <= top_range:
        if not _invalid_id(bot_range):
            logger.debug(f"{bot_range} is a valid id.")
            bot_range += 1
            continue

        logger.info(f"{bot_range} is indeed an invalid id!")
        invalid_ids.append(bot_range)
        bot_range += 1

    return invalid_ids


def _invalid_id(id_in_range: int) -> bool:
    """Validate if an ID is valid or not."""

    def is_odd_len() -> bool:
        logger.debug(f"{len(_id)=}")
        return len(_id) % 2 == 1

    _id = str(id_in_range)
    if is_odd_len():
        return False

    return _id[0 : len(_id) // 2] == _id[len(_id) // 2 :]


def _sum_invalid_ids_chunks(filename: str) -> int:
    """Sum all the invalid ids within ranges with chunks."""
    gen = _build_id_ranges(filename)
    invalid_ids = []
    for bot, top in gen:
        invalid_ids.extend(_find_invalid_ids_chunks(bot, top))
    return sum(invalid_ids)


def _find_invalid_ids_chunks(bot_range: int, top_range: int) -> list[int]:
    """Get all the invalid ids in a range."""
    invalid_ids = []
    logger.debug(f"Checking between {bot_range} and {top_range}.")
    while bot_range <= top_range:
        if not _invalid_id_chunks(bot_range):
            logger.debug(f"{bot_range} is a valid id.")
            bot_range += 1
            continue

        logger.info(f"{bot_range} is indeed an invalid id!")
        invalid_ids.append(bot_range)
        bot_range += 1

    return invalid_ids


def _invalid_id_chunks(id_in_range: int) -> bool:
    """Validate if an ID is valid or not."""
    _id = str(id_in_range)

    MAX_LENGTH = round(len(_id) // 2)
    logger.debug(f"{MAX_LENGTH=}")
    MIN_LENGTH = 1
    chunk_size = MIN_LENGTH

    while chunk_size <= MAX_LENGTH:
        logger.debug(f"Starting with chunk at size {chunk_size}.")
        if len(_id) % chunk_size != 0:
            logger.debug(f"Discarding chunk at size {chunk_size}.")
            chunk_size += 1
            continue

        chunks = len(_id) // chunk_size
        # eg 10 // 2 = 5
        chunk_index = 0

        while chunk_index < chunks:
            logger.debug(f"Cycling with chunk index {chunk_index}.")
            offset = chunk_size * chunk_index
            first_chunk = _id[0:chunk_size]
            current_chunk = _id[offset : offset + chunk_size]
            if first_chunk != current_chunk:
                logger.info(
                    f"Discarding chunk {chunk_size}. {first_chunk} != {current_chunk}"
                )
                break
            chunk_index += 1

        # if all chunks have been validated, the id in invalid
        if chunk_index == chunks:
            logger.info(
                f"Found chunks with size {chunk_size} have all matching chuncks! {first_chunk} == {current_chunk}"
            )
            return True

        chunk_size += 1

    return False


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
