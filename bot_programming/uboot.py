import sys
import math

# FIXED
MAX_MOVE_DISTANCE = 600
SINK_DISTANCE = 300
SCAN_DISTANCE = 800
SCAN_DISTANCE_LIGHT = 2000
MAX_ENERGY = 30
LIGHT_ENERGY_COST = 5

class Creature:
    def __init__(self, id=-1, coordinates=(-1,-1), speed=(-1,-1), color=-1, type=-1, scanned=0):
            self.id = id
            self.coordinates = coordinates
            self.speed = speed
            self.color = color
            self.type = type
            self.scanned = scanned

    def __str__(self):
        return f"FISH: {self.id} {self.coordinates[0]} {self.coordinates[1]} {self.speed[0]} {self.speed[1]} {self.color} {self.type}"

class Drone:
    def __init__(self, id, coordinates, emergency, battery):
        self.id = id
        self.coordinates = coordinates
        self.emergency = emergency
        self.battery = battery

    def __str__(self):
        return f"DRONE: {self.id} {self.coordinates[0]} {self.coordinates[1]} {self.emergency} {self.battery}"


def move(coordinates,light: int):
    return f'MOVE {coordinates[0]} {coordinates[1]} {light}'

def distance_between(coordinates1, coordinates2):
    return math.sqrt((coordinates2[0] - coordinates1[0])**2 + (coordinates2[1] - coordinates1[1])**2)

def find_nearest(coordinate, fishes):
    current_min_distance = 100000
    current_min_distance_id = -100000
    for fish in fishes.values():
        if fish.scanned == 0:
            distance_between_fish_and_coordinate = distance_between(coordinate, fish.coordinates)
            if distance_between_fish_and_coordinate < current_min_distance:
                current_min_distance = distance_between_fish_and_coordinate
                current_min_distance_id = fish.id
    return current_min_distance_id


creatures = {}

creature_count = int(input())
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    creatures[creature_id] = Creature(creature_id, (0,0),(0,0),color,_type)


outputstring = {}
mydrones = {}
foedrones = {}

scanned_creatures = set()
# game loop
while True:
    my_score = int(input())
    foe_score = int(input())
    my_scan_count = int(input())
    for i in range(my_scan_count):
        creature_id = int(input())
        scanned_creatures.add(creature_id)
        
    print(scanned_creatures, file=sys.stderr, flush=True)
    foe_scan_count = int(input())
    for i in range(foe_scan_count):
        creature_id = int(input())
    my_drone_count = int(input())
    for i in range(my_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        mydrones[drone_id] = Drone(drone_id, (drone_x,drone_y), emergency, battery)
    foe_drone_count = int(input())
    for i in range(foe_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        foedrones[drone_id] = Drone(drone_id, (drone_x,drone_y), emergency,battery)
    drone_scan_count = int(input())
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
    visible_creature_count = int(input())
    print(f'creature count {visible_creature_count}', file=sys.stderr, flush=True)
    for i in range(visible_creature_count):
        creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
        if creature_id in creatures:
            scanned = 1 if creature_id in scanned_creatures else 0
            creatures[creature_id].coordinates = (creature_x, creature_y)
            creatures[creature_id].speed = (creature_vx, creature_vy)
            creatures[creature_id].scanned = scanned
        else:
            print(f'ERROR: creature not in list {creature_id}', file=sys.stderr, flush=True)

    radar_blip_count = int(input())
    for i in range(radar_blip_count):
        inputs = input().split()
        drone_id = int(inputs[0])
        creature_id = int(inputs[1])
        radar = inputs[2]
    

    for mydroneid in mydrones.keys():
        nearest_fish = find_nearest(mydrones[mydroneid].coordinates,creatures)
        outputstring[mydroneid] = move(creatures[nearest_fish].coordinates,0)
        print(outputstring[mydroneid])


    outputstring = {}
    mydrones = {}
    foedrones = {}

    scanned_creatures = set()

#        print("Debug messages...", file=sys.stderr, flush=True)