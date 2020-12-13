##--- Part Two ---
##
##Before you can give the destination to the captain, you realize that the
##actual action meanings were printed on the back of the instructions the
##whole time.
##
##Almost all of the actions indicate how to move a waypoint which is relative
##to the ship's position:
##
##    Action N means to move the waypoint north by the given value.
##    Action S means to move the waypoint south by the given value.
##    Action E means to move the waypoint east by the given value.
##    Action W means to move the waypoint west by the given value.
##    Action L means to rotate the waypoint around the ship left
##    (counter-clockwise) the given number of degrees.
##    Action R means to rotate the waypoint around the ship right (clockwise)
##    the given number of degrees.
##    Action F means to move forward to the waypoint a number of times equal
##    to the given value.
##
##The waypoint starts 10 units east and 1 unit north relative to the ship. The
##waypoint is relative to the ship; that is, if the ship moves, the waypoint
##moves with it.

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
    (Rot.R, 720, Dir.W): Dir.W,
    (Rot.L, 7200, Dir.N): Dir.N,
    (Rot.R, 7200, Dir.N): Dir.N,
    }

for rtc in rotate_testcases:
    assert rotate_testcases[rtc] == rotate(*rtc)

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

    def rotate(self, r:Rot, deg:int) -> None:
        # Part 2 means this very differently.
        # It's not just rotating in place, it's rotating a vector around its origin.
        #self.dir = rotate(direction, degrees, self.dir)
        if (r, deg) in ((Rot.L, 90), (Rot.R, 270)):
            self.x, self.y = self.y, -self.x
        elif (r, deg) in ((Rot.R, 90), (Rot.L, 270)):
            self.x, self.y = -self.y, self.x
        elif (r, deg) in ((Rot.L, 180), (Rot.R, 180)):
            self.x, self.y = -self.x, -self.y

    def manhattan(self):
        return abs(self.x) + abs(self.y)

    def __repr__(self):
        return f"<Vec ({self.x}, {self.y}) {self.dir}>"

# acquire input (part 2)
ship = Vec(0,0) # ship's absolute position.
waypoint = Vec(10,-1) # ship "at origin" relative to this.
with open("input12", "r") as f:
    for line in f:
        #print("S:", ship, end='\t')
        #print("W:", waypoint)
        if line.strip():
            #print(line.strip())
            cmd = line[0]
            val = int(line[1:])
            if cmd in ("N", "E", "S", "W"):
                waypoint.translate(strdir[cmd], val)
            elif cmd in ("L", "R"):
                waypoint.rotate(strrot[cmd], val)
            elif cmd == "F":
                ship.x += waypoint.x * val
                ship.y += waypoint.y * val


print(ship.manhattan())
