##--- Part Two ---
##
##As soon as people start to arrive, you realize your mistake. People don't
##just care about adjacent seats - they care about the first seat they can
##see in each of those eight directions!
##
##Now, instead of considering just the eight immediately adjacent seats,
##consider the first seat in each of those eight directions.
##Also, people seem to be more tolerant than you expected: it now takes
##five or more visible occupied seats for an occupied seat to become empty
##(rather than four or more from the previous rules). The other rules still
##apply: empty seats that see no occupied seats become occupied, seats
##matching no rule don't change, and floor never changes.

# acquire input

import sys
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input11"

gridtxt = []
with open(filename, "r") as f:
          for line in f:
              if line.strip(): gridtxt.append([c for c in line.strip()])

# Puzzle time.
# I want to deal in Enums - the states. I'll mimic traditional cellular
# automata, i.e. Game of Life - live & dead cells - but add walls ('blocked').

# helper functions + dicts: states <-> text, print out a grid.

# I want the grid to be static, so I'll use tuples.
# Tuple[Tuple[Enum]] should be hashable, so I'll use a {parent: child} dict
# to track state transitions and look for a loop.
# Kinda according to the puzzle, when state points to self, we're done.
# In any case, when state points to an existing state, there's a loop.

# applying the transition simultaneously - in ~O(n) memory
# I'll put my faith in hashes, we don't need to store all states.
# One grid of States, one grid of ints (neighbors).
# 1st pass to count neighbors, 2nd pass to change states.
# hash() the grid, display it, continue until end condition is met.


from enum import Enum
class State(Enum):
    BLOCKED = 0
    DEAD = 1
    LIVE = 2

    def __repr__(self):
        return statetxt[self]
    
txtstate = {'.': State.BLOCKED,
            'L': State.DEAD,
            '#': State.LIVE,
            '!': None
            }

statetxt = {txtstate[k]: k for k in txtstate} # inverse

def transition(state:State, neighbors:int) -> State:
    if state == State.LIVE and neighbors >= 5: # part 2, now 5 neighbors
        return State.DEAD
    elif state == State.DEAD and neighbors == 0:
        return State.LIVE
    else: return state

from typing import List, Tuple

# Part 2 modifies this
# This would be a great candidate to clean up into a few functions.
# the 4-loops deep looks like crap. the di, dj loops in their own fn
# would make this a lot more readable.
def neighbors(grid:Tuple[Tuple[State]]) -> Tuple[Tuple[int]]:
    out = []
    for i in range(len(grid)):
        out.append([])
        for j in range(len(grid[0])):
            count = 0
            for base_di in (-1, 0, 1):
                for base_dj in (-1, 0, 1):
                    #print(f"{i}, {j} -> {base_di}, {base_dj}:", end = ' ')
                    di, dj = base_di, base_dj
                    # don't count self
                    if di == dj == 0: continue
                    # bounds checking (no grid looping)
                    elif (i + di) < 0 or (i + di) >= len(grid):
                        #print(f"out of bounds (row): {di:+},{dj:+}")
                        continue
                    elif (j + dj) < 0 or (j + dj) >= len(grid[0]):
                        #print(f"out of bounds (column): {di:+},{dj:+}")
                        continue
                    # part 2: extend our "vector" along its
                    # original line until it finds an unblocked position.
                    while grid[i + di][j + dj] == State.BLOCKED:
                        di += base_di
                        dj += base_dj
                        # found an edge? cancel vector extension
                        if (i + di) < 0 or (i + di) >= len(grid) or \
                           (j + dj) < 0 or (j + dj) >= len(grid[0]):
                            di, dj = base_di, base_dj
                            break # while loop
                    #print(f"{i},{j} considering {di},{dj} ({grid[i+di][j+dj]})")
                    if grid[i + di][j + dj] == State.LIVE: count += 1
            out[-1].append(count)
        out[-1] = tuple(out[-1])
    return tuple(out)

def parse_text(txt:Tuple[Tuple[str]]) -> Tuple[Tuple[State]]:
    out = []
    for row in txt:
        out.append([])
        for col in row:
            out[-1].append(txtstate[col])
        out[-1] = tuple(out[-1])
    return tuple(out)

from pprint import pprint

def display(grid:Tuple[Tuple[State]]) -> None:
    for row in grid:
        for col in row:
            print(statetxt[col], end='')
        print()
    print()

grid = parse_text(gridtxt)
state_transitions = {}
last_hash = None
state_history = []
this_hash = hash(grid)
print("Starting grid:")
#display(grid)

while this_hash not in state_history:
    state_history.append(this_hash)
    last_hash = this_hash
    ngrid = neighbors(grid)
    next_grid = []
    for row in range(len(grid)):
        next_grid.append([])
        for col in range(len(grid[row])):
            next_grid[-1].append(transition(grid[row][col], ngrid[row][col]))
        next_grid[-1] = tuple(next_grid[-1])
    next_grid = tuple(next_grid)
    this_hash = hash(next_grid)
    state_transitions[last_hash] = this_hash
    print(f"State #{len(state_history)}: {this_hash}")
    #display(next_grid)
    grid = next_grid

print(f"Total states: {len(state_history)}")
from collections import defaultdict
cell_totals = defaultdict(int)
for row in grid:
    for col in row:
        cell_totals[col] += 1

pprint(cell_totals)
