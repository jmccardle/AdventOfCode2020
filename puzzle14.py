##--- Part Two ---
##
##It's getting pretty expensive to fly these days - not because of ticket
##prices, but because of the ridiculous number of bags you need to buy!
##
##Consider again your shiny gold bag and the rules from the above example:
##
##    faded blue bags contain 0 other bags.
##    dotted black bags contain 0 other bags.
##    vibrant plum bags contain 11 other bags: 5 faded blue bags and 6
##    dotted black bags.
##    dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted
##    black bags.
##
##So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags
##within it) plus 2 vibrant plum bags (and the 11 bags within each of those):
##1 + 1*7 + 2 + 2*11 = 32 bags!
##
##Of course, the actual rules have a small chance of going several levels
##deeper than this example; be sure to count all of the bags, even if the
##nesting becomes topologically impractical!
##
##Here's another example:
##
##shiny gold bags contain 2 dark red bags.
##dark red bags contain 2 dark orange bags.
##dark orange bags contain 2 dark yellow bags.
##dark yellow bags contain 2 dark green bags.
##dark green bags contain 2 dark blue bags.
##dark blue bags contain 2 dark violet bags.
##dark violet bags contain no other bags.
##
##In this example, a single shiny gold bag must contain 126 other bags.

# Personal challenge part 1: starting today, be more object oriented.
# Personal challenge part 2: try to build a datastructure without seeing part 2.

from typing import Tuple, List, Dict

_colors = {} # Colors will be singletons for `is` usage
# the _colors dictionary will contain every color, exactly once.
# use the Color function to access existing colors or create on-the-fly.

class _Color:
    """A single modified color - Singleton Class"""
    __slots__ = ('modifier', 'color')

    def __init__(self, modifier:str, color:str) -> None:
        """Initializes class object and stores global singleton"""
        self.modifier = modifier
        self.color = color
        _colors[(modifier, color)] = self

    def __eq__(self, other) -> bool:
        """Ensures function of == operator; may be redundant?"""
        return isinstance(other, _Color) and \
            self.color == other.color and \
            self.modifier == other.modifier

    def __repr__(self) -> str:
        return f"<Color {self.modifier} {self.color}>"

    def __hash__(self) -> int:
        """For use as dict keys"""
        return hash((self.modifier, self.color))

def Color(modifier:str, color:str) -> _Color:
    """Color singleton access method. Returns or creates _Color objects"""
    if (modifier, color) in _colors: return _colors[(modifier, color)]
    return _Color(modifier, color)

class Rule: # pre-defined for recursive usage as a defined type
    pass

class Rule:
    """A single rule about containment requirements"""
    __slots__ = ('color', 'contains')
    def __init__(self, color:_Color, contains:Dict[_Color, int]) -> None:
        self.color = color
        self.contains = contains

    def __repr__(self) -> str:
        return f"<Rule `{self.color}`, contains {self.contains}>"

    def can_hold(self, color:_Color) -> int:
        if color not in self.contains: return 0
        return self.contains[color]

    def total_hold(self) -> int:
        """All the subbags directly held. If 0, this is a "leaf" bag."""
        return sum(self.contains.values())

    def recursive_hold(self, rules:Dict[_Color, Rule]) -> int:
        subcontents = [rules[c].recursive_hold(rules) * self.contains[c] for c in self.contains]
        #print(self.color, [z for z in zip(subcontents, self.contains.keys())], self.total_hold() + sum(subcontents))
        return self.total_hold() + sum(subcontents)

def line_to_rule(line:str) -> Rule:
    rcolor, ccolors = line.split(" bags contain ")
    r_color = Color(*rcolor.split(' ')) #'clear grey' to '<Color clear grey>'
    if "no other bags" in ccolors: return Rule(r_color, {})
    qtycolors = {}
    for qtycolor in ccolors.split(','):
        # '1 bright grey bag' to '{<Color bright grey>: 1}'
        qtycolor = qtycolor.strip()
        #print(qtycolor)
        qty, mod, ccol, _ = qtycolor.split(' ')
        qtycolors[Color(mod, ccol)] = int(qty)
    return Rule(r_color, qtycolors)

def can_contain(rules:Dict[_Color, Rule], tcolor:_Color) -> int:
    to_investigate = set()
    # first pass: these colors can hold the target color directly
    for rc in _colors.values():
        if rules[rc].can_hold(tcolor): to_investigate.add(rc)

    investigated = set()
    # repeated pass:
    # * ignore already investigated colors
    # * add and notate any that could hold a to_investigate color
    while True:
        found_this_loop = 0
        print(f"Investigated: {len(investigated)} To investigate: {len(to_investigate)}")
        #print(to_investigate)
        for rc in _colors.values():
            if rc in investigated: continue
            if any([rules[rc].can_hold(c) for c in to_investigate]):
                to_investigate.add(rc)
                investigated.add(rc)
                found_this_loop += 1
        if not found_this_loop:
            break # end infinite loop
    return to_investigate

# Main program execution
if __name__ == '__main__':
    filename = "input7"
    
    rules = {}
    # Acquire input - convert to objects line by line
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not len(line): continue # skip blanks
            rule = line_to_rule(line)
            rules[rule.color] = rule

    print(f"Loaded data: {len(rules)} rules and {len(_colors)} unique colors.")

    # solve part 1
    target_color = Color('shiny', 'gold')
    #hold_set = can_contain(rules, target_color)
    #print(f"Could hold a {target_color} bag: {len(hold_set)}")

    # solve part 2
    print(rules[target_color].recursive_hold(rules))
