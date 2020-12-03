##Each policy actually describes two positions in the password, where 1 means
##the first character, 2 means the second character, and so on. (Be careful;
##Toboggan Corporate Policies have no concept of "index zero"!) Exactly one
##of these positions must contain the given letter. Other occurrences of the
##letter are irrelevant for the purposes of policy enforcement.
##
##Given the same example list from above:
##
##    1-3 a: abcde is valid: position 1 contains a and position 3 does not.
##    1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
##    2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
##
##How many passwords are valid according to the new interpretation of the
##policies?

# Acquire puzzle input. "input2" is saved from the website.
# Rules are not unique. Originally I tried a dictionary, but that failed.

pwdatabase = []

with open("input2", "r") as f:
    for line in f:
        key, val = line.split(':')
        pwdatabase.append( (key.strip(), val.strip()) )

# Problem solving. Does a password match its rule?
# Puzzle 4 based on Puzzle 3 - these are positions, not ranges.

### Bugs I encountered ###

# Off-by-one error checking: is it +1 or -1 to the index?
# I could stop and think about it, but there's only options to try.
# Well, +1 gave an index out of bounds error, so it's probably -1...

# Boo-boo #2: One position "or" (exclusive or) the other.
# Python doesn't have keyword xor, so `(statement) ^ (statement)` will work.
# `test == value ^ test == value` won't, because bitwise xor is before ==.
# A rare case where the order of prescedence didn't work out for me.

def is_valid(rule:str, password:str) -> bool:
    minmax, letter = rule.split(' ')
    p1, p2 = [int(m) for m in minmax.split('-')]
    #print(f"pw: {password} p1: {p1} p2: {p2} letter: {letter} pw[p1]: {password[p1-1]} pw[p2]: {password[p2-1]}")
    return (password[p1-1] == letter) ^ (password[p2-1] == letter)

# I'm just guessing at this point, but I bet the second problem handles
# similar data. So I'm going to sort the passwords, not just count them.

valid_passes = []
invalid_passes = []
for rule, pw in pwdatabase:
    if is_valid(rule, pw):
        valid_passes.append( (rule, pw) )
    else:
        invalid_passes.append( (rule, pw) )

print(f"""Valid passwords: {len(valid_passes)}""")
