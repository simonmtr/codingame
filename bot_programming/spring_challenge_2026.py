import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

MAX_HEIGHT = 11
MAX_WIDTH = MAX_HEIGHT * 2

def get_distance(coord1: tuple, coord2: tuple) -> int:
    return abs(coord1[0]-coord2[0]) + abs(coord1[1] - coord2[1])

def printdebug(message:str):
    print(message, file=sys.stderr, flush=True)

class Tree:
    def __init__(self, coord: tuple, treetype: str, health: int, fruits: int, cooldown: int, size: int):
        self.coord = coord
        self.type = treetype
        self.health = health
        self.fruits = fruits
        self.cooldown = cooldown
        self.size = size
        

class TreeService:
    def __init__(self):
        self.all_trees = {}
        self.harvestable = {}
        self.max_size = {}

    def append_tree(self, tree: Tree):
        if tree.fruits > 0:
            self.harvestable[tree.coord] = tree
        elif tree.size == 4:
            self.max_size[tree.coord] = tree
        else:
            self.all_trees[tree.coord] = tree

class Troll:
    def __init__(self, id: int, coord: tuple, movspeed: float, carry_cap: int, harvest: int, chop: int, carry_sum: int, carrying: dict):
        self.id = id
        self.coord = coord
        self.movspeed = movspeed
        self.carry_cap = carry_cap
        self.harvest = harvest
        self.chop = chop
        self.carry_sum = carry_sum
        self.carrying = carrying

    def check_for_base_return(self, base: tuple[int, int]):
        if self.check_for_drop(base=base):
            return None
        min_dist = MAX_HEIGHT * MAX_WIDTH
        printdebug(f'base: {base}')
        droplocations = [
            (base[0] + 1, base[1]),
            (base[0] - 1, base[1]),
            (base[0], base[1] + 1),
            (base[0], base[1] - 1),
        ]
        min_coord = (-2, -2)
        if self.carry_sum == self.carry_cap:
            for loc in droplocations:
                cur_dist = get_distance(loc, self.coord)
                if cur_dist < min_dist:
                    min_coord = loc
                    min_dist = cur_dist
            return min_coord
        return None

    def check_for_drop(self, base: tuple[int, int]):
        droplocations = [
            (base[0] + 1, base[1]),
            (base[0] - 1, base[1]),
            (base[0], base[1] + 1),
            (base[0], base[1] - 1),
        ]
        printdebug(f"coord: {self.coord} | carry: {self.carry_sum}")
        if self.coord in droplocations and self.carry_sum > 0:
            return True
        return False
    
    def check_for_harvest(self, trees: TreeService):
        if self.coord in trees.harvestable and self.carry_sum < self.carry_cap:
            return True
        return False
    
    def get_closest_tree(self, trees: TreeService) -> tuple[int, int]:
        min_diff = MAX_HEIGHT * MAX_WIDTH
        min_diff_coord = (-1, -1)
        exp_harvest = 0
        for coord, tree in trees.harvestable.items():
            dist = get_distance(self.coord, tree.coord)
            if min_diff > dist and (exp_harvest < tree.fruits or tree.fruits > self.carry_cap):
                min_diff = dist
                min_diff_coord = coord
                exp_harvest = tree.fruits
        if exp_harvest > 0:
            printdebug(f"harvesting: {min_diff_coord}")
            return min_diff_coord
        for coord, tree in trees.max_size.items():
            dist = get_distance(self.coord, tree.coord)
            if tree.cooldown > (dist/self.movspeed) and min_diff > dist and exp_harvest == 0:
                min_diff = dist
                min_diff_coord = coord
                exp_harvest = tree.fruits
        printdebug(f"going to: {min_diff_coord}")
        return min_diff_coord

class Player:
    def __init__(self, trolls: dict[int, Troll], inventory: dict):
        self.trolls = trolls
        self.inventory = inventory
        self.base: tuple[int, int] = (0,0)

    def set_base(self, coord: tuple[int, int]):
        self.base = coord

    
def movecommand(trollid: int, coord: tuple):
    return f"MOVE {trollid} {coord[0]} {coord[1]}"

def harvestcommand(trollid: int):
    return f"HARVEST {trollid}"

def dropcommand(trollid: int):
    return f"DROP {trollid}"


own_player = Player(trolls={}, inventory={})
enemy_player = Player(trolls={}, inventory={})
grass: dict = {}



width, height = [int(i) for i in input().split()]
for i in range(height):
    line = input()
    for c in range(len(line)):
        coord = (c, i)
        if line[c] == "0":
            own_player.set_base(coord)
        elif line[c] == "1":
            enemy_player.set_base(coord)
        elif line[c] == ".":
            grass[coord] = "GRASS"

# game loop
first_round = True
while True:
    commands = []
    trees: TreeService = TreeService()


    for i in range(2):
        plum, lemon, apple, banana, iron, wood = [int(j) for j in input().split()]
        if i == 1:
            own_player.inventory = {'plum': plum,'lemon':lemon,'apple': apple,'banana': banana,'iron': iron, 'wood': wood}
        elif i == 2:
            enemy_player.inventory = {'plum': plum,'lemon':lemon,'apple': apple,'banana': banana,'iron': iron, 'wood': wood}

    trees_count = int(input())
    for i in range(trees_count):
        inputs = input().split()
        _type = inputs[0]
        x = int(inputs[1])
        y = int(inputs[2])
        size = int(inputs[3])
        health = int(inputs[4])
        fruits = int(inputs[5])
        cooldown = int(inputs[6])
        trees.append_tree(Tree(coord=(x, y), treetype=_type, health=health, fruits=fruits, cooldown=cooldown, size=size))
    trolls_count = int(input())
    for i in range(trolls_count):
        _id, player, x, y, movement_speed, carry_capacity, harvest_power, chop_power, carry_plum, carry_lemon, carry_apple, carry_banana, carry_iron, carry_wood = [int(j) for j in input().split()]
        if player == 0:
            carrying = {'plum': carry_plum,'lemon':carry_lemon,'apple': carry_apple,'banana': carry_banana,'iron': carry_iron, 'wood': carry_wood}
            carry_sum = carry_plum + carry_lemon + carry_apple + carry_banana + carry_iron + carry_wood 
            own_player.trolls[_id] = Troll(id=_id, coord=(x, y), movspeed=movement_speed, carry_cap=carry_capacity, harvest=harvest_power, chop=chop_power, carry_sum=carry_sum, carrying=carrying)
            base_return = own_player.trolls[_id].check_for_base_return(base=own_player.base)
            if base_return:
                commands.append(movecommand(trollid=_id, coord=base_return))
            elif own_player.trolls[_id].check_for_drop(base=own_player.base):
                commands.append(dropcommand(trollid=_id))
            elif own_player.trolls[_id].check_for_harvest(trees=trees):
                commands.append(harvestcommand(trollid=_id))
            else: # MOVE
                coord = own_player.trolls[_id].get_closest_tree(trees=trees)
                commands.append(movecommand(trollid=_id, coord=coord))

        elif player == 1:
            pass
    # Write an action using print
    first_round = False
    

    # valid actions:
    # MOVE <id> <x> <y>
    # HARVEST <id> - when you are on the same cell as a tree
    # DROP <id> - when you are next to your shack and carry items
    outputstring = ""
    for command in commands:
        outputstring += command + ";"
    print(outputstring)

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
