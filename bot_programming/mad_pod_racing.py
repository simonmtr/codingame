import sys
import math

# print
printstring = ''
# static
checkpoint_radius = 600
max_x = 16000
max_y = 9000

class Checkpoint:
    def __init__(self, x, y, distance, angle):
        self.x = x
        self.y = y
        self.distance = distance
        self.angle = angle
    def __str__(self):
        return f"{self.x} {self.y} {self.distance} {self.angle}"
# movement
def printdebug(printstring):
    print(printstring, file=sys.stderr, flush=True)

def printboost(coordinates):
    global printstring
    printstring += f"{coordinates[0]} {coordinates[1]} BOOST"

def printshield(coordinates):
    global printstring
    printstring += f"{coordinates[0]} {coordinates[1]} SHIELD"
    
def printthrust(coordinates, value):
    global printstring
    printstring += f"{coordinates[0]} {coordinates[1]} {value}"

# movement decisions
def boost_or_thrust():
    printdebug('boostorthrust')



# variables
my_pods = []
opponent_pods = []
next_checkpoint = ''

# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    my_pods.append((x,y))
    next_checkpoint = Checkpoint(next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle)
    opponent_x, opponent_y = [int(i) for i in input().split()]
    opponent_pods.append((opponent_x, opponent_y))

    printdebug('aa')
    printdebug(str(next_checkpoint))




    print(str(next_checkpoint.x) + " " + str(next_checkpoint.y) + " BOOST")
    print(str(next_checkpoint.x) + " " + str(next_checkpoint.y) + " 100")
