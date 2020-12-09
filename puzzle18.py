##The final step in breaking the XMAS encryption relies on the invalid number
##you just found: you must find a contiguous set of at least two numbers in
##your list which sum to the invalid number from step 1.
##
##Again consider the above example (file `input9t`):
##
##In this list, adding up all of the numbers from 15 through 40 produces the
##invalid number from step 1, 127. (Of course, the contiguous set of numbers
##in your actual list might be much longer.)
##
##To find the encryption weakness, add together the smallest and largest
##number in this contiguous range; in this example, these are 15 and 47,
##producing 62.
##
##What is the encryption weakness in your XMAS-encrypted list of numbers?

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

    def search_preamblesum(self):
        for i, n in enumerate(self.numbers[self.preamble_length:]):
            n_valid = self.is_valid(i+self.preamble_length)
            #print(f"{i+self.preamble_length}: {n} {n_valid}")
            if not n_valid: return n

    def search_contig(self, value):
        for i, n in enumerate(self.numbers):
            reach = 1
            while i+reach < len(self.numbers) and \
                  sum(self.numbers[i:i+reach]) < value:
                reach += 1
            if sum(self.numbers[i:i+reach]) == value:
                return self.numbers[i:i+reach]

if __name__ == '__main__':
    numbers = []
    with open("input9", "r") as f:
        for line in f:
            if line.strip(): numbers.append(int(line))

    s = sumquence(numbers, 25)
    #print(numbers)
    search_value = s.search_preamblesum()
    subset = s.search_contig(search_value)
    print(subset)
    print(min(subset) + max(subset))
