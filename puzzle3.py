##For example, suppose you have the following list:
##
##1-3 a: abcde
##1-3 b: cdefg
##2-9 c: ccccccccc
##
##Each line gives the password policy and then the password. The password
##policy indicates the lowest and highest number of times a given letter
##must appear for the password to be valid. For example, 1-3 a means that
##the password must contain a at least 1 time and at most 3 times.
##
##In the above example, 2 passwords are valid. The middle password, cdefg,
##is not; it contains no instances of b, but needs at least 1. The first
##and third passwords are valid: they contain one a or nine c, both within
##the limits of their respective policies.
##
##How many passwords are valid according to their policies?

# Acquire puzzle input. "input2" is saved from the website.

### Bug I encountered ###
# Rules are not unique. Originally I tried a dictionary, but that failed.

pwdatabase = []

with open("input2", "r") as f:
    for line in f:
        key, val = line.split(':')
        pwdatabase.append( (key.strip(), val.strip()) )

# Problem solving. Does a password match its rule?

def is_valid(rule:str, password:str) -> bool:
    minmax, letter = rule.split(' ')
    mn, mx = [int(m) for m in minmax.split('-')]
    #print(f"pw: {password} min: {mn} max: {mx} letter: {letter} count: {password.count(letter)} {mn} <= {password.count(letter)} <= {mx}: {mn <= password.count(letter) <= mx}")
    return mn <= password.count(letter) <= mx

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
