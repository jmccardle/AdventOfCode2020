#Advent of Code Puzzle #1

## The Elves in accounting are thankful for your help; one of them even offers
## you a starfish coin they had left over from a past vacation. They offer you
## a second one if you can find three numbers in your expense report that meet
## the same criteria.
##
## Using the above example again, the three entries that sum to 2020 are 979,
## 366, and 675. Multiplying them together produces the answer, 241861950.
##
## In your expense report, what is the product of the three entries that sum
## to 2020?

# Acquire puzzle input. "input1" is saved from the website.

numbers = []

with open("input1", "r") as f:
    for line in f:
        numbers.append(int(line))

# Sort numbers. There's no sequence to them, so this lets me make some assumptions.
numbers.sort()

# Thinking cap time...
# This is really similar, and I'm just going to brute force the "middle" number.
from typing import Tuple

def search(lst, target=2020) -> Tuple[int, int, int, int]:
    """Searches a list for two numbers that sum to a target.
        Assumes a sorted list.
        Counts the number of tests performed (so speedup can be calculated).
        Output: tuple(number1, number2, total_tests, indexes_checked)"""
    total_checks = 0
    i_checks = 0
    for i in lst:
        i_checks += 1
        #print(f"Searching on {i}. Total checks: {total_checks}")
        for j in lst[::-1]:
            for k in lst[::-1]:
                total_checks += 1
                if i + j + k > target: continue # next k
                if i + j + k < target: break # next j
                if i + j + k == target: return i, j, k, total_checks, i_checks
        

# Prepare some output.

i, j, k, total_checks, i_checks = search(numbers)
print(f"Total checks: {total_checks} -> {1 - (total_checks / 100**3):.2%} total savings, {(i_checks / 100):.0%} indexes checked (less = lucky)")

print(f"{i} + {j} + {k} = 2020; {i} * {j} * {k} = {i*j*k}")
