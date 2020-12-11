##--- Part Two ---
##
##To completely determine whether you have enough adapters, you'll need to
##figure out how many different ways they can be arranged. Every arrangement
##needs to connect the charging outlet to your device. The previous rules
##about when adapters can successfully connect still apply.
##
##The first example above (the one that starts with 16, 10, 15) supports the
##following arrangements:
##
##(0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
##(0), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
##(0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
##(0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
##(0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
##(0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
##(0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
##(0), 1, 4, 7, 10, 12, 15, 16, 19, (22)
##
##(The charging outlet and your device's built-in adapter are shown in
##parentheses.) Given the adapters from the first example, the total
##number of arrangements that connect the charging outlet to your device
##is 8.
##
##The second example above (the one that starts with 28, 33, 18) has many
##arrangements. Here are a few:
##
##(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
##32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49, (52)
##
##(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
##32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 49, (52)
##
##(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
##32, 33, 34, 35, 38, 39, 42, 45, 46, 48, 49, (52)
##
##(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
##32, 33, 34, 35, 38, 39, 42, 45, 46, 49, (52)
##
##(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
##32, 33, 34, 35, 38, 39, 42, 45, 47, 48, 49, (52)
##
##(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
##46, 48, 49, (52)
##
##(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
##46, 49, (52)
##
##(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
##47, 48, 49, (52)
##
##(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
##47, 49, (52)
##
##(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
##48, 49, (52)
##
##In total, this set of adapters can connect the charging outlet to your
##device in 19208 distinct arrangements.
##
##You glance back down at your bag and try to remember why you brought so
##many adapters; there must be more than a trillion valid ways to arrange
##them! Surely, there must be an efficient way to count the arrangements.
##
##What is the total number of distinct ways you can arrange the adapters
##to connect the charging outlet to your device?

import sys
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input10t2"

# Acquire input
joltages = []
with open(filename, "r") as f:
    for line in f:
        if line.strip(): joltages.append(int(line))

# (Part 1) Strategy.
# Wall = 0. Device = max(joltages) + 3.
# Don't we just sort the dang thing?
joltages.insert(0, 0) # wall
#joltages.append(max(joltages) + 3) # device

joltages.sort()

#(part 1 solution)
from collections import defaultdict
differences = defaultdict(lambda: 0)
for i, j in enumerate(joltages[:-1]):
    diff = joltages[i+1] - j
    differences[diff] += 1

from pprint import pprint
pprint(dict(differences))
print(differences[1] * differences[3])


# (Part 2) Strategy.
# Sort, but determine which can be skipped.
# if we have 1, 2, and 3 in the set... 1, 2, or 3 could be the next step.
# Branch and count the final valid branches.

nodes_created = 0

class Node:
    def __init__(self, payload):
        global nodes_created
        nodes_created += 1
        self.children = None
        self.payload = payload

    def propagate(self, successorfn):
        self.children = [Node(v) for v in successorfn(self.payload)]
        for c in self.children: c.propagate(successorfn)

    def count_walk(self, criterion):
        if len(self.children) == 0: return int(criterion(self.payload))
        return int(criterion(self.payload)) + sum([c.count_walk(criterion) for c in self.children])
        
    def __repr__(self):
        return f"<Node value {self.payload}, {len(self.children) if self.children else 'no'} children>"

#def joltage_successors(value):
#    node_index = joltages.index(value)
#    return [i for i in joltages[node_index+1:] if i <= value+3]

def joltage_successor(lst):
    return lambda value: [i for i in lst[lst.index(value)+1:] if i <= value+3]

def joltage_criterion(target):
    return lambda value: value == target

def fixed_point_sublists(full_list):
    def farthest_member(n):
        return max([i for i in joltages if i <= n+3])
    farthest = {n: farthest_member(n) for n in full_list}
    #print(farthest)
    targets = list(farthest.values())
    fixed_points = []
    for v in set(farthest.values()):
        if targets.count(v) > 1:
            fixed_points.append(v)
            
    #print("Fixed points: ", fixed_points)
    print("[", end='')
    for i in full_list:
        print(f"{i}->{farthest[i]}{'*' if i in fixed_points else ''}{', ' if i != full_list[-1] else ''}", end='')
    print("]")
    prev_index = 0
    fixed_points.sort()
    for v in fixed_points:
        next_index = full_list.index(v)
        print(f"{v} <- [{next_index}]")
        yield full_list[prev_index:next_index+1]
        prev_index = next_index

sublists = [l for l in fixed_point_sublists(joltages)]

#root = Node(joltages[0])

#root.propagate(joltage_successors)
#val = root.count_walk(joltage_criterion)

#print(root)
#print(val)
#print(nodes_created)

factors = []
for sl in sublists:
    # successor function: +3 rule against this list
    suc = joltage_successor(sl)
    # root of the tree
    root = Node(sl[0])
    # propogation: create entire (sublist) tree
    root.propagate(suc)
    # counting: count all nodes that match this list
    crit = joltage_criterion(sl[-1])
    factors.append(root.count_walk(crit))
    print(root)
    print("factors: ", factors)
    print("node total: ", nodes_created)
    
from functools import reduce
print(reduce(lambda x, y: x*y, factors))
