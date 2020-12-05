##It's a completely full flight, so your seat should be the only missing
##boarding pass in your list. However, there's a catch: some of the seats
##at the very front and back of the plane don't exist on this aircraft,
##so they'll be missing from your list as well.
##
##Your seat wasn't at the very front or back, though; the seats with IDs
##+1 and -1 from yours will be in your list.

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

def sid_to_rc(i:int) -> Tuple[int, int]:
    row = int(bin(i)[:-3],2)
    col = int(bin(i)[-3:],2)
    return (row, col)

for rc in numerical_passes:
    assert sid_to_rc(seat_id(*rc)) == rc

# Having made it to this point, I can reverse any seat ID accurately

numerical_passes.sort(key = lambda rc: seat_id(*rc))
rows = set([r for r,c in numerical_passes])
for this_r in rows:
    taken_seats = set([c for r,c in numerical_passes if r == this_r])
    # Graphical solution (helped me work it out)
    #diagram = ''.join([str(n) if n in taken_seats else 'x' for n in range(8)])
    #flag = "\t*** OPEN SEAT: ***" if 'x' in diagram else ''
    #print(f"row: {this_r} seats: {diagram}{flag}")
    for n in range(8):
        if all((n not in taken_seats, n-1 in taken_seats, n+1 in taken_seats)):
            print(f"Available seat: Row {this_r}, Seat {n}, ID {seat_id(this_r,c)}")
