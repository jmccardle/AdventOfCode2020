##The navigation instructions (your puzzle input) consists of a sequence of
##single-character actions paired with integer input values. After staring at
##them for a few minutes, you work out what they probably mean:
##
##    Action N means to move north by the given value.
##    Action S means to move south by the given value.
##    Action E means to move east by the given value.
##    Action W means to move west by the given value.
##    Action L means to turn left the given number of degrees.
##    Action R means to turn right the given number of degrees.
##    Action F means to move forward by the given value in the direction the
##ship is currently facing.
##
##The ship starts by facing east. Only the L and R actions change the
##direction the ship is facing. (That is, if the ship is facing east and
##the next instruction is N10, the ship would move north 10 units, but would
##still move east if the following action were F.)

from enum import Enum

class Dir(Enum):
    E, N, W, S = 0, 90, 180, 270

strdir = {"N": Dir.N, "E": Dir.E, "S": Dir.S, "W": Dir.W}

class Rot(Enum):
    L, R = 1, -1

strrot = {"L": Rot.L, "R": Rot.R}

def rotate(direction:Rot, degrees:int, start_direction:Dir) -> Dir:
    if direction == Rot.R: degrees *= -1
    degrees += start_direction.value
    degrees = ((degrees % 360) + 360) % 360
    return Dir(degrees)

rotate_testcases = {
    (Rot.L, 90, Dir.N): Dir.W,
    (Rot.R, 90, Dir.N): Dir.E,
    (Rot.L, 180, Dir.S): Dir.N,
    (Rot.R, 720, Dir.W): Dir.W
    }

class Vec:
    tvecs = {Dir.E: (1, 0), Dir.N: (0, -1), Dir.W: (-1, 0), Dir.S: (0, 1)}
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = Dir.E

    def translate(self, direction:Dir, distance:int) -> None:
        dx, dy = Vec.tvecs[direction]
        dx *= distance; dy *= distance
        self.x += dx; self.y += dy

    def rotate(self, direction:Rot, degrees:int) -> None:
        self.dir = rotate(direction, degrees, self.dir)

    def manhattan(self):
        return abs(self.x) + abs(self.y)

# acquire input
ship = Vec(0,0)
with open("input12", "r") as f:
    for line in f:
        if line.strip():
            cmd = line[0]
            val = int(line[1:])
            if cmd in ("N", "E", "S", "W"):
                ship.translate(strdir[cmd], val)
            elif cmd in ("L", "R"):
                ship.rotate(strrot[cmd], val)
            elif cmd == "F":
                ship.translate(ship.dir, val)

print(ship.manhattan())
