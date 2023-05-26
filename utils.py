import logging
import os
from enum import Enum
from pathlib import Path

BASE_PATH = Path(__file__).parent
LOGGER_NAME = "AOC"

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1

def setup_logger(level: LogLevel) -> logging.Logger:
    """Creates a logger instance."""
    logger = logging.Logger(LOGGER_NAME)
    logger.setLevel(level.value)
    logger.addHandler(_logger_handler())

    return logger

def _logger_handler() -> logging.StreamHandler:
    """Setup the default stream handler."""
    log_format = 'VERBOSE:: %(message)s-%(funcName)s-%(name)s-%(lineno)d'
    formatter = logging.Formatter(log_format)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    return handler

def create_log_level(debug: bool) -> LogLevel:
    """Factory for logging level."""
    if debug:
        return LogLevel.DEBUG
    return LogLevel.INFO

def load_input_data(day: str, debug: bool = False) -> list[str]:
    """Load all data from a file."""
    data_file = f"{day}_input.txt"
    if debug:
        data_file = f"{day}_example.txt"
    data_path = BASE_PATH / "input_data" / data_file

    if not os.path.exists(data_path):
        raise ValueError(f"Unable to find {data_path} file!")

    with open(data_path, "r") as f:
        lines = f.readlines()

    return [line.replace("\n", "") for line in lines]
