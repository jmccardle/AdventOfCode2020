##--- Part Two ---
##
##After some careful analysis, you believe that exactly one instruction is
##corrupted.
##
##Somewhere in the program, either a jmp is supposed to be a nop, or a nop
##is supposed to be a jmp. (No acc instructions were harmed in the corruption
##                          of this boot code.)
##
##The program is supposed to terminate by attempting to execute an instruction
##immediately after the last instruction in the file. By changing exactly one
##jmp or nop, you can repair the boot code and make it terminate correctly.
##
##For example, consider the same program from above:
##
##nop +0
##acc +1
##jmp +4
##acc +3
##jmp -3
##acc -99
##acc +1
##jmp -4
##acc +6
##
##If you change the first instruction from nop +0 to jmp +0, it would create
##a single-instruction infinite loop, never leaving that instruction. If you
##change almost any of the jmp instructions, the program will still eventually
##find another jmp instruction and loop forever.
##
##However, if you change the second-to-last instruction (from jmp -4 to nop -4),
##the program terminates! The instructions are visited in this order:
##
##nop +0  | 1
##acc +1  | 2
##jmp +4  | 3
##acc +3  |
##jmp -3  |
##acc -99 |
##acc +1  | 4
##nop -4  | 5
##acc +6  | 6
##
##After the last instruction (acc +6), the program terminates by attempting to
##run the instruction below the last instruction in the file. With this change,
##after the program terminates, the accumulator contains the value 8 (acc +1,
##acc +1, acc +6).
##
##Fix the program so that it terminates normally by changing exactly one jmp
##(to nop) or nop (to jmp). What is the value of the accumulator after the
##program terminates?

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
    TERM    = 3

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
        if self.pointer >= len(self.program):
            print("Program terminated")
            return Errorcode.TERM
        instruction = self.program[self.pointer]
        if instruction.sequence:
            #print("Loop detected - program halted")
            return Errorcode.INFLOOP
        elif self.pointer < 0:
            #print("invalid position - program halted")
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

    def reset(self) -> None:
        self.accumulator = 0
        self.pointer = 0
        self.steps = 0
        for i in self.program:
            i.sequence = None

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

    #Part 1's solution
    print("Final accumulator value:", tm.accumulator)

    #Part 2's solution
    # Identify suspect instructions for swapping
    suspects = []
    for index, i in enumerate(tm.program):
        if not i.sequence: continue
        if i.opcode == OpCode.JMP or i.opcode == OpCode.NOP:
            suspects.append(index)

    def flip_opcode(instruction) -> None:
        if instruction.opcode == OpCode.JMP:
            instruction.opcode = OpCode.NOP
        elif instruction.opcode == OpCode.NOP:
            instruction.opcode = OpCode.JMP
        else:
            raise Exception("erroneous suspect - ", instruction)

    modified = None # restore between attempts

    for index, i in enumerate(suspects):
        if modified:
            flip_opcode(tm.program[modified])
        flip_opcode(tm.program[i])
        modified = i
        tm.reset()
        ec = Errorcode.NOERROR
        while ec == Errorcode.NOERROR:
            ec = tm.step()
        if ec == Errorcode.TERM:
            print("Program exited normally; solution found")
            break
        else: print(f"Suspect cleared: {i} ({index} / {len(suspects)})")

    print("Final accumulator value:", tm.accumulator)
    
        
