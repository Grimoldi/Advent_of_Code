import os

from utils import load_input_data

DAY = os.path.basename(__file__).split(".")[0]


def main():
    nums = find_sums()
    # first question
    find_max_sum(nums, 1)
    # second question
    find_max_sum(nums, 3)


def find_sums(debug: bool = False) -> list[int]:
    """Loads the data and find the total for each elf."""
    lines = load_input_data(DAY, debug)

    sum = 0
    maxs = []

    for line in lines:

        if line == "":
            maxs.append(sum)
            sum = 0
            continue

        else:
            num = int(line)
            sum += num

    return sorted(maxs, reverse=True)


def find_max_sum(nums: list[int], pos: int) -> None:
    """Finds the first pos sum."""
    print(sum(nums[0:pos]))


if __name__ == "__main__":
    main()
