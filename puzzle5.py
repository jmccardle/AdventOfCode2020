##The locations you'd check in the above example are marked here with O where
##there was an open square and X where there was a tree:
##
##..##.........##.........##.........##.........##.........##.......  --->
###..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
##.#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
##..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
##.#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
##..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
##.#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
##.#........#.#........X.#........#.#........#.#........#.#........#
###.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
###...##....##...##....##...#X....##...##....##...##....##...##....#
##.#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
##
##In this example, traversing the map using this slope would cause you to
##encounter 7 trees.
##
##Starting at the top-left corner of your map and following a slope of right
##3 and down 1, how many trees would you encounter?


# Acquire input
with open("input3", "r") as f:
    rows = f.read().split('\n')


# Problem solving time.
#  * The 'y' coordinate is our current row.
#  * The 'x' coordinate is our current row, modulus the row width.
#    The rows are of fixed width, but I think they could repeat fine if not.

## Bug Encountered ##
# "if not len(row)" and "if len(row)" in the function/lambda respectively:
# The last line of the file ends in a newline; this is interpreted as a blank line.
# len(row) == 0 in that case, and causes a div by zero.

def trees_encountered(x_rate:int, y_rate:int=1) -> int:
    trees = 0
    for i, row in enumerate(rows):
        if not len(row): continue
        if i % y_rate: continue # skip row if not falling 1 at a time
        here = row[(i * x_rate) % len(row)]
        trees += 1 if here == '#' else 0
    return trees

# could compress:
t_e = lambda xr, yr=1: sum([1 for i, row in enumerate(rows) if len(row) and not i % yr and row[(i * xr) % len(row)] == '#'])

print(trees_encountered(3))
print(t_e(3))
