from __future__ import annotations

import math
import os
from dataclasses import dataclass, field

from utils import load_input_data

DAY = os.path.basename(__file__).split(".")[0]


@dataclass
class Strategy:
    divisible_test: int
    operation: str


@dataclass
class Monkey:
    name: str
    true_friend: Monkey = field(init=False, repr=False)
    false_friend: Monkey = field(init=False, repr=False)
    true_friend_name: str
    false_friend_name: str
    strategy: Strategy
    business_score: int
    items: list[int] = field(default_factory=list)
    debug: bool = False
    lmc: int = field(init=False)

    def add_true_friend(self, monkey: Monkey) -> None:
        """Setter method."""
        self.true_friend = monkey

    def add_false_friend(self, monkey: Monkey) -> None:
        """Setter method."""
        self.false_friend = monkey

    def add_item(self, item: int) -> None:
        """Setter method."""
        self.items.append(item)

    def add_lmc(self, lmc: int) -> None:
        """Setter method."""
        self.lmc = lmc

    def get_business_score(self) -> int:
        """Getter method."""
        return self.business_score

    def play_round(self, should_i_worry: bool = False) -> None:
        """Monkey plays a round."""
        if self.debug:
            print(f"\tMonkey {self.name} has items {[x for x in self.items]}.\n")
        for self._item in self.items:
            new_worry_level = self._inspect_item()
            if should_i_worry:
                new_worry_level = self._relief(new_worry_level)
            test = self._test_item(new_worry_level)
            if test:
                self._thrown_item(new_worry_level, self.true_friend)
            else:
                self._thrown_item(new_worry_level, self.false_friend)
        self._empty_hands()

    def _inspect_item(self) -> int:
        """Inspect an item."""
        if self.debug:
            print(
                f"\tMonkey {self.name} inspects an item with a worry level of {self._item}"
            )
        old = self._item
        new_worry_level = eval(self.strategy.operation)
        reduced_worry_level = self.lmc + (new_worry_level % self.lmc)
        self._increment_business_score()
        if self.debug:
            print(
                f"\tWorry level is raised to {new_worry_level}, then reduced to {reduced_worry_level}."
            )
        return reduced_worry_level

    def _increment_business_score(self) -> None:
        """Increments the business score of the monkey."""
        self.business_score += 1

    def _relief(self, item: int) -> int:
        """Relief after monkey gets bored."""
        new_worry_level = item // 3
        if self.debug:
            print(
                f"\tMonkey {self.name} gets bored. New worry level {new_worry_level}."
            )
        return new_worry_level

    def _test_item(self, item: int) -> bool:
        """Monkey test the item against the strategy."""
        if self.debug:
            print(
                f"\t{item} divisible by {self.strategy.divisible_test}: {self._item % self.strategy.divisible_test == 0}"
            )
        return item % self.strategy.divisible_test == 0

    def _thrown_item(self, item: int, monkey: Monkey) -> None:
        """Monkey throws the item."""
        if self.debug:
            print(
                f"\tItem with worry level {item} is thrown to monkey {monkey.name}.\n"
            )
        monkey.add_item(item)

    def _empty_hands(self) -> None:
        """Monkey has thrown all items."""
        self.items = list()


def load_monkeys(debug: bool = False) -> list[Monkey]:
    """Loads the monkeys from the input file."""
    lines = load_input_data(DAY, debug)
    monkeys: list[Monkey] = list()
    monkey_lines: list[str] = list()
    for line in lines:
        if line.startswith("Monkey"):
            monkey_lines = list()

        if line != "":
            monkey_lines.append(line)
            continue

        monkeys.append(create_monkey(monkey_lines))

    common_lmc = get_lmc([x.strategy for x in monkeys])
    for monkey in monkeys:
        monkey.add_true_friend(find_monkey_friend(monkeys, monkey.true_friend_name))
        monkey.add_false_friend(find_monkey_friend(monkeys, monkey.false_friend_name))
        monkey.add_lmc(common_lmc)
    return monkeys


def create_monkey(lines: list[str], debug: bool = False) -> Monkey:
    """Creates a Monkey instance."""
    for line in lines:
        line = line.strip()
        if line.startswith("Monkey"):
            name = get_name(line)
        elif line.startswith("Starting"):
            items = get_items(line)
        elif line.startswith("Operation"):
            operation = get_operation(line)
        elif line.startswith("Test"):
            test = get_test(line)
        elif line.startswith("If true"):
            true_friend = get_friend(line)
        elif line.startswith("If false"):
            false_friend = get_friend(line)

    strategy = Strategy(test, operation)  # type: ignore
    business_score = 0
    return Monkey(name, true_friend, false_friend, strategy, business_score, items, debug)  # type: ignore


def get_name(line: str) -> str:
    """Gets a monkey name."""
    return line.replace("Monkey", "").replace(":", "").strip()


def get_items(line: str) -> list[int]:
    """Gets the starting items of a monkey."""
    line = line.replace("Starting items: ", "").replace(",", "")
    return [int(item) for item in line.split(" ")]


def get_operation(line: str) -> str:
    """Gets the operation of a monkey."""
    return line.replace("Operation: new = ", "")


def get_test(line: str) -> int:
    """Gets the test of a monkey."""
    return int(line.replace("Test: divisible by ", ""))


def get_friend(line: str) -> str:
    """Gets the friend of a monkey."""
    return line.replace("If true: throw to monkey ", "").replace(
        "If false: throw to monkey ", ""
    )


def find_monkey_friend(monkeys: list[Monkey], name: str) -> Monkey:
    """Gets a Monkey instance from a monkey name."""

    for monkey in monkeys:
        if name == monkey.name:
            return monkey

    raise ValueError(f"Unable to find {name} in {[x.name for x in monkeys]}")


def get_lmc(monkeys_strategy: list[Strategy]) -> int:
    """Finds the lmc against all divisible tests."""
    return math.lcm(*[x.divisible_test for x in monkeys_strategy])


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    monkeys = load_monkeys(debug)
    business_scores = list()
    ROUNDS = 20

    for index in range(ROUNDS):
        if debug:
            print(f"Round {index}")
        for monkey in monkeys:
            monkey.play_round(True)

            if index == ROUNDS - 1:
                business_scores.append(monkey.get_business_score())
                print(
                    f"Monkey {monkey.name} has a business score of {monkey.get_business_score()}"
                )

    business_scores.sort(reverse=True)

    print(
        f"First question answer. The business score of the top two monkeys is {business_scores[0] * business_scores[1]}."
    )


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    monkeys = load_monkeys(debug)
    business_scores = list()
    ROUNDS = 10_000

    for index in range(ROUNDS):
        if debug:
            print(f"Round {index}")
        for monkey in monkeys:
            monkey.play_round(False)

            if index == ROUNDS - 1:
                business_scores.append(monkey.get_business_score())
                print(
                    f"Monkey {monkey.name} has a business score of {monkey.get_business_score()}"
                )

    business_scores.sort(reverse=True)
    print(f"{business_scores}")
    print(
        f"Second question answer. The business score of the top two monkeys is {business_scores[0] * business_scores[1]}."
    )


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
