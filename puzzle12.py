#part 2

groups = []
with open("input6", "r") as f:
    thisgroup = []
    #personsingroup = []
    for line in f: 
        if line.strip() == "":
            groups.append(thisgroup)
            thisgroup = []

        # adding empty lines as members causes intersection errors, obviously
        if len(line.strip()): thisgroup.append(set([c for c in line.strip()]))
    groups.append(thisgroup)

# This is the "long form" code I needed to work out the chain intersectioning
intersections = []
for g in groups:
	inters = g[0] # 'red flag 1' for using "reduce": setting to first member
	for member in g[1:]: # 'red flag 2' for using "reduce": looping over [1:]
		inters=inters.intersection(member)
		# 'red flag 3' for using "reduce": overwriting working variable
	intersections.append(inters)

# This can be turned into a reduce:
from functools import reduce
isections = [reduce(lambda g1, g2: g1.intersection(g2), g) for g in groups]

print(sum([len(g) for g in intersections]))
print(sum([len(g) for g in isections]))
