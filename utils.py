import os
from pathlib import Path

BASE_PATH = Path(__file__).parent


def load_input_data(day: str, debug: bool = False) -> list[str]:
    """Load all matches from a file."""
    data_file = f"{day}_input.txt"
    if debug:
        data_file = f"{day}_example.txt"
    data_path = BASE_PATH / "input_data" / data_file

    if not os.path.exists(data_path):
        raise ValueError(f"Unable to find {data_path} file!")

    with open(data_path, "r") as f:
        lines = f.readlines()

    return [line.replace("\n", "") for line in lines]
