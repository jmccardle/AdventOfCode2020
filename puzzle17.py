##Here is a larger example which only considers the previous 5 numbers (and has
##a preamble of length 5): (see file `input9t`)
##
##In this example, after the 5-number preamble, almost every number is the sum
##of two of the previous 5 numbers; the only number that does not follow this
##rule is 127.
##
##The first step of attacking the weakness in the XMAS data is to find the first
##number in the list (after the preamble) which is not the sum of two of the 25
##numbers before it. What is the first number that does not have this property?

class sumquence:
    def __init__(self, numbers, preamble_length=25):
        self.numbers = numbers
        self.preamble_length = preamble_length

    def preamble(self):
        return self.numbers[:preamble_length]

    def is_valid(self, index):
        for n in self.numbers[index-self.preamble_length:index]:
            requirement = self.numbers[index] - n
            #print(f"  n: {n} requirement: {requirement} in: {self.numbers[index-self.preamble_length:index]}")
            if requirement in self.numbers[index-self.preamble_length:index]: return True
        return False

    def search(self):
        for i, n in enumerate(self.numbers[self.preamble_length:]):
            n_valid = self.is_valid(i+self.preamble_length)
            #print(f"{i+self.preamble_length}: {n} {n_valid}")
            if not n_valid: return n

if __name__ == '__main__':
    numbers = []
    with open("input9", "r") as f:
        for line in f:
            if line.strip(): numbers.append(int(line))

    s = sumquence(numbers, 25)
    #print(numbers)
    result = s.search()
    print(result)
