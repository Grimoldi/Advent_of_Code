from __future__ import annotations

import os
import pprint
from dataclasses import dataclass, field

from utils import load_input_data

DAY = os.path.basename(__file__).split(".")[0]


@dataclass
class Tree:
    height: int

    def __str__(self) -> str:
        return f"{self.height}"

    def __gt__(self, other: Tree) -> bool:
        return self.height > other.height

    def __ge__(self, other: Tree) -> bool:
        return self.height >= other.height

    def __lt__(self, other: Tree) -> bool:
        return self.height < other.height

    def __eq__(self, other: Tree) -> bool:
        return self.height == other.height


@dataclass
class TreeGrid:
    width: int
    height: int

    def __post_init__(self) -> None:
        self.grid = [[0] * self.width for _ in range(self.height)]
        self.pp = pprint.PrettyPrinter(indent=4, width=160)

    def add_tree(self, tree: Tree, x: int, y: int) -> None:
        """Adds a Tree to the grid."""
        self.grid[x][y] = tree  # type: ignore

    def row(self, row: int) -> list[Tree] | list[int]:
        """Returns a given row of the grid."""
        return self.grid[row]

    def col(self, col: int) -> list[Tree] | list[int]:
        """Returns a given column of the grid."""
        return [row[col] for row in self.grid]

    def print_grid(self) -> None:
        """Prints the grid."""
        for row in self.grid:
            for col in row:
                print(f"{col} ", end="")
            print()
        # self.pp.pprint(self.grid)

    def get_neighbourhood(self, row: int, col: int) -> list[list[Tree]]:
        """From a tree position, get the tree up, bot, right and left to it, from in to out."""
        rows = self.row(row)
        cols = self.col(col)
        left = rows[0:col]
        right = rows[col + 1 : len(cols) + 1]
        top = cols[0:row]
        bot = cols[row + 1 : len(rows) + 1]

        return [[x for x in reversed(left)], right, [x for x in reversed(top)], bot]  # type: ignore

    def is_visible(self, row: int, col: int) -> bool:
        """Finds out if a tree is visible from outside."""
        tree = self.grid[row][col]

        dirs = self.get_neighbourhood(row, col)
        for dir in dirs:
            if dir == list():
                return True  # outer trees are always visible

            max_tree = max(dir)
            if tree > max_tree:  # type: ignore
                return True
        return False

    def get_scenic_score(self, row: int, col: int, debug: bool = False) -> int:
        """Get the scenic score from a given position."""
        tree = self.grid[row][col]

        scenic_score = 1
        dirs = self.get_neighbourhood(row, col)
        for dir in dirs:
            if dir == list():
                continue
            for index, other_tree in enumerate(dir, start=1):
                if other_tree >= tree:  # type: ignore
                    if debug:
                        print(
                            f"Found bigger tree {other_tree} {tree}. {index} {scenic_score}"
                        )
                    scenic_score = scenic_score * index
                    break

                if index == len(dir):
                    if debug:
                        print(f"End of the list. {index} {scenic_score}")
                    scenic_score = scenic_score * index

        return scenic_score


def fill_grid(data: list[list[str]], grid: TreeGrid) -> None:
    """Fills the grid with each tree."""
    for x, row in enumerate(data):
        for y, tree_height in enumerate(row):
            new_tree = Tree(int(tree_height))
            grid.add_tree(new_tree, x, y)


def find_visible_trees(grid: TreeGrid, width: int, height: int) -> int:
    """Finds out how many tree are visible in a given grid."""
    total = 0
    for x in range(width):
        for y in range(height):
            if grid.is_visible(x, y):
                total += 1

    return total


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    data = load_input_data(DAY, debug)
    if debug:
        width, height = (5, 5)
    else:
        width, height = (99, 99)
    grid = TreeGrid(width, height)
    fill_grid(data, grid)  # type: ignore
    if debug:
        grid.print_grid()
    visible_trees = find_visible_trees(
        grid,
        width,
        height,
    )
    print(f"First question answer. The visible trees are: {visible_trees}")


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    data = load_input_data(DAY, debug)
    if debug:
        width, height = (5, 5)
    else:
        width, height = (99, 99)
    grid = TreeGrid(width, height)
    fill_grid(data, grid)  # type: ignore
    if debug:
        grid.print_grid()
        print(grid.get_scenic_score(3, 2, True))
    scores = list()
    for x in range(width):
        for y in range(height):
            if x * y != 0 or x != width or y != width:
                scores.append(grid.get_scenic_score(x, y, debug))
    print(f"Second question answer. The most scenic tree has a score of: {max(scores)}")


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
