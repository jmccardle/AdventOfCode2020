##Due to recent aviation regulations, many rules (your puzzle input) are being
##enforced about bags and their contents; bags must be color-coded and must
##contain specific quantities of other color-coded bags. Apparently, nobody
##responsible for these regulations considered how long they would take to
##enforce!
##
##For example, consider the following rules:
##
##light red bags contain 1 bright white bag, 2 muted yellow bags.
##dark orange bags contain 3 bright white bags, 4 muted yellow bags.
##bright white bags contain 1 shiny gold bag.
##muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
##shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
##dark olive bags contain 3 faded blue bags, 4 dotted black bags.
##vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
##faded blue bags contain no other bags.
##dotted black bags contain no other bags.
##
##These rules specify the required contents for 9 bag types. In this example,
##every faded blue bag is empty, every vibrant plum bag contains 11 bags (5
##faded blue and 6 dotted black), and so on.
##
##You have a shiny gold bag. If you wanted to carry it in at least one other
##bag, how many different bag colors would be valid for the outermost bag?
##(In other words: how many colors can, eventually, contain at least one shiny
## gold bag?)
##
##In the above rules, the following options would be available to you:
##
##    A bright white bag, which can hold your shiny gold bag directly.
##    A muted yellow bag, which can hold your shiny gold bag directly, plus
##    some other bags.
##    A dark orange bag, which can hold bright white and muted yellow bags,
##    either of which could then hold your shiny gold bag.
##    A light red bag, which can hold bright white and muted yellow bags,
##    either of which could then hold your shiny gold bag.
##
##So, in this example, the number of bag colors that can eventually contain
##at least one shiny gold bag is 4.
##
##How many bag colors can eventually contain at least one shiny gold bag?
##(The list of rules is quite long; make sure you get all of it.)

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

def line_to_rule(line):
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
    hold_set = can_contain(rules, target_color)
    print(f"Could hold a {target_color} bag: {len(hold_set)}")
