##For example, consider just the first seven characters of FBFBBFFRLR:
##
##    Start by considering the whole range, rows 0 through 127.
##    F means to take the lower half, keeping rows 0 through 63.
##    B means to take the upper half, keeping rows 32 through 63.
##    F means to take the lower half, keeping rows 32 through 47.
##    B means to take the upper half, keeping rows 40 through 47.
##    B keeps rows 44 through 47.
##    F keeps rows 44 through 45.
##    The final F keeps the lower of the two, row 44.
##
##The last three characters will be either L or R; these specify exactly one
##of the 8 columns of seats on the plane (numbered 0 through 7). The same
##process as above proceeds again, this time with only three steps. L means
##to keep the lower half, while R means to keep the upper half.
##
##For example, consider just the last 3 characters of FBFBBFFRLR:
##
##    Start by considering the whole range, columns 0 through 7.
##    R means to take the upper half, keeping columns 4 through 7.
##    L means to take the lower half, keeping columns 4 through 5.
##    The final R keeps the upper of the two, column 5.
##
##So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
##
##Every seat also has a unique seat ID: multiply the row by 8, then add the
##column. In this example, the seat has ID 44 * 8 + 5 = 357.
##
##Here are some other boarding passes:
##
##    BFFFBBFRRR: row 70, column 7, seat ID 567.
##    FFFBBBFRRR: row 14, column 7, seat ID 119.
##    BBFFBBFRLL: row 102, column 4, seat ID 820.
##
##As a sanity check, look through your list of boarding passes. What is the
##highest seat ID on a boarding pass?

# acquire input
passes = []
with open("input5", "r") as f:
    for line in f: passes.append(line.strip())

from typing import Tuple

row_key = {'F': '0', 'B': '1'}
col_key = {'L': '0', 'R': '1'}

def alpha_to_bin(code:str, key:dict) -> int:
    s = ''.join([key[c] for c in code]) # swap letters from decoding dictionary
    return int(s, 2) # treat as binary text

def bsp_to_rowcol(code: str) -> Tuple[int, int]:
    row = alpha_to_bin(code[:-3], row_key)
    col = alpha_to_bin(code[-3:], col_key)
    return row, col

#onelineify
bsp_rc = lambda s: (int(s[:-3].replace('F', '0').replace('B', '1'),2), int(s[-3:].replace('L', '0').replace('R', '1'),2))

numerical_passes = [bsp_to_rowcol(s) for s in passes]
np = [bsp_rc(s) for s in passes]

def seat_id(row:int, col:int) -> int:
    return row * 8 + col

validation = {
    'FBFBBFFRLR': (44, 5, 357),
    'BFFFBBFRRR': (70, 7, 567),
    'FFFBBBFRRR': (14, 7, 119),
    'BBFFBBFRLL': (102, 4, 820)
    }

for s in validation:
    r, c = bsp_to_rowcol(s)
    i = seat_id(r, c)
    r2, c2 = bsp_rc(s)
    i2 = seat_id(r2, c2)
    assert (r, c, i) == (r2, c2, i2)
    assert (r, c, i) == validation[s]

# Having made it to this point, all example inputs are matched by my code

print(max([seat_id(*s) for s in numerical_passes]))
