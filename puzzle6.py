##Determine the number of trees you would encounter if, for each of the following slopes,
##you start at the top-left corner and traverse the map all the way to the bottom:
##
##    Right 1, down 1.
##    Right 3, down 1. (This is the slope you already checked.)
##    Right 5, down 1.
##    Right 7, down 1.
##    Right 1, down 2.
##
##In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s) respectively;
##multiplied together, these produce the answer 336.
##
##What do you get if you multiply together the number of trees encountered on each of
##the listed slopes?


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

slopes = [ (1, 1), (3, 1), (5, 1), (7, 1), (1, 2) ]
prod = 1
for xr, yr in slopes:
    te = trees_encountered(xr, yr)
    prod *= te
    print(f"({xr},{yr}): {te}")

print(prod)
