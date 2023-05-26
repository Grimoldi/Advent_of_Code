from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

import utils

DAY = os.path.basename(__file__).split(".")[0]


@dataclass
class File:
    """Dataclass that represents a single file."""

    name: str
    size: int


@dataclass
class DirectoryTree:
    """Dataclass that represents a single folder."""

    name: str
    parent: DirectoryTree | None = field(default=None)
    directories: list[DirectoryTree] = field(default_factory=list, init=False)
    files: list[File] = field(default_factory=list, init=False)

    def add_subfolder(self, folder: DirectoryTree) -> None:
        """Add a folder as a subfolder."""
        self.directories.append(folder)

    def remove_subfolder(self, folder: DirectoryTree) -> None:
        """Remove a folder from a directory tree."""
        try:
            self.directories.remove(folder)
        except ValueError:
            raise ValueError(f"Folder {folder.name} cannot be found!")

    def add_file(self, file: File) -> None:
        """Add a file in the directory."""
        self.files.append(file)

    def remove_file(self, file: File) -> None:
        """Remove a file from a directory tree."""
        try:
            self.files.remove(file)
        except ValueError:
            raise ValueError(f"File {file.name} cannot be found!")

    @property
    def size(self) -> int:
        size = 0
        for file in self.files:
            size += file.size
        for directory in self.directories:
            size += directory.size
        return size

    @property
    def path(self) -> str:
        if not self.parent:
            return f"{self.name}"
        if not self.parent.parent:
            return f"{self.parent.path}{self.name}"
        return f"{self.parent.path}/{self.name}"


def create_folder_tree(lines: list[str], debug: bool = False) -> DirectoryTree:
    """From a line describe if it's a move, a directory or a file."""
    tree = DirectoryTree(name="/")
    current_folder = tree

    for line in lines:
        # print(f"Path: {current_folder.path}, cmd: {line}")
        if line == "$ cd /":
            continue  # skip first line

        elif is_upper_tree(line):  # cd ..
            current_folder = move_up(current_folder)

        elif is_deeper_tree(line):  # cd <folder>
            name = line.replace(r"$ cd ", "")
            current_folder = change_folder(name, current_folder)

        elif is_list_files(line):  # ls
            continue

        elif is_dir(line):  # dir <folder>
            name = line.replace("dir ", "")
            subfolder = DirectoryTree(name, parent=current_folder)
            current_folder.add_subfolder(subfolder)

        elif is_file(line):  # <size> <filename>
            size, name = line.split(" ")
            current_file = File(name, int(size))  # type: ignore
            current_folder.add_file(current_file)

    return tree


def is_deeper_tree(line: str) -> bool:
    """Finds if the current line is a 'cd <dir>' command."""
    if re.search(r"\$ cd \w+", line):
        return True
    return False


def is_upper_tree(line: str) -> bool:
    """Finds if the current line is a 'cd .. 'command."""
    if re.search(r"\$ cd \.\.", line):
        return True
    return False


def is_list_files(line: str) -> bool:
    """Finds if the current line is an ls command."""
    if re.search(r"\$ ls", line):
        return True
    return False


def is_dir(line: str) -> bool:
    """Finds if the current line is a dir."""
    if re.search(r"dir .*", line):
        return True
    return False


def is_file(line: str) -> bool:
    """Finds if the current line is a file."""
    if re.search(r"\d+ \w+", line):
        return True
    return False


def move_up(tree: DirectoryTree) -> DirectoryTree:
    """Move one level up in the folder tree."""
    if tree.parent:
        return tree.parent
    raise ValueError("Unable to go up of one level!")


def change_folder(folder_name: str, tree: DirectoryTree) -> DirectoryTree:
    """Change directory in the folder tree."""
    for directory in tree.directories:
        if directory.name == folder_name:
            return directory

    raise ValueError(f"Unable to find the subfolder {folder_name} under {tree}.")


def list_folders(tree: DirectoryTree) -> list[DirectoryTree]:
    """Creates a list for all folders from a given tree."""
    folders = list()
    for folder in tree.directories:
        folders.append(folder)
        folders.extend(list_folders(folder))

    return folders


def filter_folder_greater_than_size(
    folders: list[DirectoryTree], size: int
) -> list[DirectoryTree]:
    """Filters only folder that have a size greater than the threshold."""

    return [folder for folder in folders if folder.size > size]


def filter_folder_lesser_than_size(
    folders: list[DirectoryTree], size: int
) -> list[DirectoryTree]:
    """Filters only folder that have a size lesser than the threshold."""

    return [folder for folder in folders if folder.size < size]


def print_tree(tree: DirectoryTree, indent: int = 0) -> None:
    """Prints the tree with indentation for each level."""
    delimiter = "  "
    tabs = delimiter * indent
    print(f"{tabs}{tree.path} ({tree.size})")
    for file in tree.files:
        new_tabs = delimiter * (indent + 1)
        print(f"{new_tabs}{file.name} ({file.size})")
    indent += 1
    for folder in tree.directories:
        print_tree(folder, indent)


def first_question(debug: bool = False) -> None:
    """Function to solve the first question."""
    FILTER_SIZE = 100_000
    data = utils.load_input_data(DAY, debug)
    tree = create_folder_tree(data, debug)

    folders = list_folders(tree)
    filtered_folders = filter_folder_lesser_than_size(folders, FILTER_SIZE)
    folders_sum = sum([folder.size for folder in filtered_folders])
    print(
        f"First question answer. "
        f"The total size of the folder lesser than {FILTER_SIZE} is: {folders_sum}"
    )
    if debug:
        print_tree(tree)


def second_question(debug: bool = False) -> None:
    """Function to solve the second question."""
    TOTAL_DISK_SIZE = 70_000_000
    UPDATE_SIZE = 30_000_000
    data = utils.load_input_data(DAY, debug)
    tree = create_folder_tree(data, debug)
    used_space = tree.size
    space_to_freed = (used_space + UPDATE_SIZE) - TOTAL_DISK_SIZE

    folders = list_folders(tree)
    filtered_folders = filter_folder_greater_than_size(folders, space_to_freed)
    sorted_folders = sorted(filtered_folders, key=lambda x: x.size, reverse=False)
    smallest_folder = sorted_folders[0]

    print(
        f"Second question answer. "
        f"The smallest folder that can be deleted to free up {space_to_freed} is: "
        f"{smallest_folder.path} ({smallest_folder.size})."
    )
    if debug:
        print_tree(tree)


def main() -> None:
    first_question()
    second_question()


if __name__ == "__main__":
    main()
