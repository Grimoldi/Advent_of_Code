import os
import re
import sys
from collections import deque
from dataclasses import dataclass

from utils import load_input_data

DAY = os.path.basename(__file__).split(".")[0]


def setup_queues(debug: bool = False) -> list[deque]:
    """Setup each LIFO queues from the input file."""
    if debug:
        stacks = 3
    else:
        stacks = 9
    queues = list()
    for _ in range(stacks):
        new_queue = deque()
        queues.append(new_queue)

    lines = load_input_data(DAY, debug)
    for line in lines:
        if line[0:3] == " 1 ":
            break
        elements = find_elem_by_stack(line)
        queues = fill_queues(elements, queues)

    return queues


def find_elem_by_stack(line: str) -> list[str]:
    """From a line, find each elements of the different stacks."""
    capacity = len(line) // 4 + 1
    index = 0
    elements = list()
    while index < capacity:
        start = index * 4
        end = (index + 1) * 4
        elem = line[start:end]
        if "[" in elem:
            item = elem.strip().replace("[", "").replace("]", "")
        else:
            item = ""
        elements.append(item)
        index += 1

    return elements


def fill_queues(elements: list[str], queues: list[deque]) -> list[deque]:
    """Sort each element in the correct stack."""
    for index, element in enumerate(elements):
        if element != "":
            queues[index].append(element)

    return queues


@dataclass
class Move:
    quantity: int
    from_queue: int
    to_queue: int


def find_moves(debug: bool = False) -> list[Move]:
    """Find the moves from the input file."""
    lines = load_input_data(DAY, debug)
    moves = list()
    data_compiler = re.compile(
        r"move (?P<how_many>\d+) from (?P<from_queue>\d) to (?P<to_queue>\d)$"
    )
    for line in lines:
        if not line.startswith("move"):
            continue

        regex_groups = data_compiler.search(line)
        try:
            how_many = int(regex_groups.group("how_many"))  # type: ignore
            from_queue = int(regex_groups.group("from_queue"))  # type: ignore
            to_queue = int(regex_groups.group("to_queue"))  # type: ignore
            moves.append(Move(how_many, from_queue, to_queue))  # type: ignore
        except AttributeError as e:
            print(f"{e=}, {line=}")
            sys.exit(119)

    return moves


def make_move_cratemover_9000(move: Move, queues: list[deque]) -> list[deque]:
    """Perform a move across the list of queues with the CrateMover 9000."""
    queue_from = queues[move.from_queue - 1]
    queue_to = queues[move.to_queue - 1]
    moves = move.quantity

    for _ in range(moves):
        top_element = queue_from.popleft()
        queue_to.appendleft(top_element)

    return queues


def make_move_cratemover_9001(move: Move, queues: list[deque]) -> list[deque]:
    """Perform a move across the list of queues with the CrateMover 9001."""
    queue_from = queues[move.from_queue - 1]
    queue_to = queues[move.to_queue - 1]
    moves = move.quantity

    crates = list()
    for _ in range(moves):
        top_element = queue_from.popleft()
        crates.insert(0, top_element)

    for crate in crates:
        queue_to.appendleft(crate)

    return queues


def print_stacks_top(queues: list[deque]) -> None:
    """Print the top of each stack."""
    for queue in queues:
        print(queue[0], end="")


def first_question() -> None:
    """Function to solve the first question."""
    queues = setup_queues()
    moves = find_moves()
    for move in moves:
        queues = make_move_cratemover_9000(move, queues)
    print_stacks_top(queues)
    print(f"\nFirst question answer. The top of each stack is: {queues}")


def second_question() -> None:
    """Function to solve the second question."""
    queues = setup_queues()
    moves = find_moves()
    for move in moves:
        queues = make_move_cratemover_9001(move, queues)
    print_stacks_top(queues)
    print(f"\nSecond question answer. The top of each stack is: {queues}")


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
