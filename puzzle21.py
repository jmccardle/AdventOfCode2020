##The seat layout fits neatly on a grid. Each position is either floor (.),
##an empty seat (L), or an occupied seat (#). For example, the initial seat
##layout might look like this:
##
##L.LL.LL.LL
##LLLLLLL.LL
##L.L.L..L..
##LLLL.LL.LL
##L.LL.LL.LL
##L.LLLLL.LL
##..L.L.....
##LLLLLLLLLL
##L.LLLLLL.L
##L.LLLLL.LL
##
##Now, you just need to model the people who will be arriving shortly.
##Fortunately, people are entirely predictable and always follow a simple
##set of rules. All decisions are based on the number of occupied seats
##adjacent to a given seat (one of the eight positions immediately up,
##down, left, right, or diagonal from the seat). The following rules are
##applied to every seat simultaneously:
##
##    If a seat is empty (L) and there are no occupied seats adjacent to it,
##    the seat becomes occupied.
##    If a seat is occupied (#) and four or more seats adjacent to it are also
##    occupied, the seat becomes empty.
##    Otherwise, the seat's state does not change.

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
    
txtstate = {'.': State.BLOCKED,
            'L': State.DEAD,
            '#': State.LIVE,
            '!': None
            }

statetxt = {txtstate[k]: k for k in txtstate} # inverse

def transition(state:State, neighbors:int) -> State:
    if state == State.BLOCKED:
        return State.BLOCKED
    elif state == State.LIVE and neighbors >= 4:
        return State.DEAD
    elif state == State.DEAD and neighbors == 0:
        return State.LIVE
    else: return state

from typing import List, Tuple

def neighbors(grid:Tuple[Tuple[State]]) -> Tuple[Tuple[int]]:
    out = []
    for i in range(len(grid)):
        out.append([])
        for j in range(len(grid[0])):
            count = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    # don't count self
                    if di == dj == 0: continue
                    # bounds checking (no grid looping)
                    elif (i + di) < 0 or (i + di) >= len(grid): continue
                    elif (j + dj) < 0 or (j + dj) >= len(grid[0]): continue
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

while this_hash != last_hash:
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
cell_totals = defaultdict(lambda: 0)
for row in grid:
    for col in row:
        cell_totals[col] += 1

pprint(cell_totals)
