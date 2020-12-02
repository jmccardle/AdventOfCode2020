#Advent of Code Puzzle #1

##they need you to find the two entries that sum to 2020 and then multiply those
## two numbers together.
##For example, suppose your expense report contained the following:
##
##1721
##979
##366
##299
##675
##1456
##
##In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying
## them together produces 1721 * 299 = 514579, so the correct answer is 514579.
##Of course, your expense report is much larger. Find the two entries that sum
## to 2020; what do you get if you multiply them together?

# Acquire puzzle input. "input1" is saved from the website.

numbers = []

with open("input1", "r") as f:
    for line in f:
        numbers.append(int(line))

# Sort numbers. There's no sequence to them, so this lets me make some assumptions.
numbers.sort()

# Thinking cap time...
# worst case scenario, try all number pairs. 100 * 99 things to consider.
# Since they're sorted, we can cut that down a lot.

# i = current index (going forward)
# j = current index (going backwards)
# for each i, start at the back of the array.
#    if i+j > 2020, step.
#    if i+j < 2020, continue. Only a subsequent i could work.
#    if i+j = 2020, break / complete the challenge.

# If I was feeling especially efficient, I would binary search for j.
# But instead, let's just brute force it. There's only 100 numbers.
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
        print(f"Searching on {i}. Total checks: {total_checks}")
        for j in lst[i::-1]:
            total_checks += 1
            if i + j > target: continue # next j
            if i + j < target: break # next i
            if i + j == target: return i, j, total_checks, i_checks
        

# Prepare some output.

i, j, total_checks, i_checks = search(numbers)
print(f"Total checks: {total_checks} -> {1 - (total_checks / 10000):.2%} total savings, {(i_checks / 100):.0%} indexes checked (less = lucky)")

print(f"{i} + {j} = 2020; {i} * {j} = {i*j}")
