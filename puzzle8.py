##You can continue to ignore the cid field, but each other field has strict
##rules about what values are valid for automatic validation:
##
##    byr (Birth Year) - four digits; at least 1920 and at most 2002.
##    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
##    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
##    hgt (Height) - a number followed by either cm or in:
##        If cm, the number must be at least 150 and at most 193.
##        If in, the number must be at least 59 and at most 76.
##    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
##    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
##    pid (Passport ID) - a nine-digit number, including leading zeroes.
##    cid (Country ID) - ignored, missing or not.
##
##Your job is to count the passports where all required fields are both present
##and valid according to the above rules.


# Acquire input
## Bug Discovered ##
# the last line may not end with newline. It's still a valid passport.
passports = []

with open("input4", "r") as f:
    pspt = {} # individual passport
    for line in f:
        line = line.strip()
        if line == "": # blank lines separate passports
            passports.append(pspt)
            pspt = {}
            continue
        for clause in line.split(' '):
            k, v = clause.split(':')
            pspt[k] = v
    if len(pspt): passports.append(pspt) # final block
            
# problem solving
# I'd like to keep the validation as data, so I can modify it next challenge
mandatory_fields = {
    'byr': True,
    'iyr': True,
    'eyr': True,
    'hgt': True,
    'hcl': True,
    'ecl': True,
    'pid': True,
    'cid': False
}
def is_valid(pspt:dict, mf:dict=mandatory_fields) -> bool:    
    return all([(f in pspt) for f in mf if mf[f]])

import string # hexdigits for 'hcl'

def hgt_valid(f):
    """The only one I couldn't do satisfactorily as a 1-liner"""
    if f.endswith('cm'):
        return 150 <= int(f[:-2]) <= 193
    elif f.endswith('in'):
        return 59 <= int(f[:-2]) <= 76
    else:
        return False

field_validations = {
    'byr': lambda f: len(f) == 4 and 1920 <= int(f) <= 2002,
    'iyr': lambda f: len(f) == 4 and 2010 <= int(f) <= 2020,
    'eyr': lambda f: len(f) == 4 and 2020 <= int(f) <= 2030,
    'hgt': hgt_valid,
    'hcl': lambda f: len(f) == 7 and all([c in string.hexdigits for c in f[1:]]),
    'ecl': lambda f: f in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
    'pid': lambda f: len(f) == 9 and f.isdigit(),
    'cid': lambda f: True
}

def is_valid_data(pspt:dict, fv:dict=field_validations) -> bool:
    # This deserves breaking out.
    # fv[f] : looks in the field_validations dict above to get a lambda (validation function)
    # pspt[f] : looks in the passport for the value of the field
    # fv[f](pspt[f]) : calls the field-specific validation function on the field's value
    # all([...] for f in pspt]) : returns True only if every field passes the check above
    return all([fv[f](pspt[f]) for f in pspt])

valid = 0
data_valid = 0
invalid = 0
for pspt in passports:
    if is_valid(pspt):
        valid += 1
        if is_valid_data(pspt): data_valid += 1
    else: invalid += 1

print(f"Total passports: {len(passports)}")
print(f"Valid format passports: {valid}")
print(f"Valid data passports: {data_valid}")
