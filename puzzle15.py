

from enum import Enum
from typing import List

class OpCode(Enum):
    NOP = 0
    ACC = 1
    JMP = 2

class Instruction:
    __slots__ = ('opcode', 'value', 'sequence')

    def __init__(self, opcode:OpCode, value:int) -> None:
        self.opcode = opcode
        self.value = value
        self.sequence = None

    def __repr__(self) -> str:
        seqstr = "{:03d}".format(self.sequence) if self.sequence else '---'
        return f"<Instruction {self.opcode} {self.value:+} #{seqstr}>"

class Errorcode(Enum):
    NOERROR = 0
    INFLOOP = 1
    INVPTR  = 2

class TapeMachine:
    __slots__ = ('accumulator', 'pointer', 'program', 'steps')

    def __init__(self, program:List[Instruction]) -> None:
        self.program = program
        self.accumulator = 0 # memory value
        self.pointer = 0 # program index
        self.steps = 0 # number of instructions executed

    def dump(self) -> None:
        print(f"step # {self.steps} pointer: {self.pointer} accumulator: {self.accumulator}")

    def step(self) -> Errorcode:
        self.steps += 1 # 1-indexing to match example input exactly.
        instruction = self.program[self.pointer]
        if instruction.sequence:
            print("Loop detected - program halted")
            return Errorcode.INFLOOP
        elif self.pointer < 0:
            print("Jump to invalid position - program halted")
            return Errorcode.INVPTR
        instruction.sequence = self.steps
        if instruction.opcode == OpCode.NOP:
            self.pointer += 1
        elif instruction.opcode == OpCode.ACC:
            self.accumulator += instruction.value
            self.pointer += 1
        elif instruction.opcode == OpCode.JMP:
            self.pointer += instruction.value
        return Errorcode.NOERROR

def line_to_instruction(line:str) -> Instruction:
    opstring, valstring = line.split(' ')
    opcode = {'nop': OpCode.NOP, 'acc': OpCode.ACC, 'jmp': OpCode.JMP}[opstring]
    value = int(valstring)
    return Instruction(opcode, value)

from pprint import pprint # for my convenience while testing
if __name__ == '__main__':

    instructions = []
    with open("input8", "r") as f:
        for line in f:
            if line.strip(): instructions.append(line_to_instruction(line))

    tm = TapeMachine(instructions)
    ec = Errorcode.NOERROR
    while ec == Errorcode.NOERROR:
        ec = tm.step()
        #tm.dump()

    #pprint(tm.program)
    print("Final accumulator value:", tm.accumulator)
