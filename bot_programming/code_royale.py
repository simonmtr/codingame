import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def calculatePythagoras(x1, y1, x2, y2):
    return math.sqrt(abs(x1-x2)*abs(x1-x2)+abs(y1-y2)*abs(y1-y2))

def getDistanceToMyQueenLastTurn(site_x, site_y):
    return calculatePythagoras(queen_x, queen_y, site_x, site_y)

sites_coordinates = {}
sites_information = {}
move_x = 0
move_y = 0
queen_x = 0
queen_y = 0
sites_with_baracks_knights = []
sites_with_baracks_archer = []
num_of_my_archers = 0
num_of_baracks_total = 0

first_round = True
base_x = 0
base_y = 0
queen_health = 100

num_sites = int(input())
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites_coordinates[site_id] = [x, y, radius]

# game loop
while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]

    min_distance_to_queen = 5000
    for i in range(num_sites):
        # ignore_1: used in future leagues
        # ignore_2: used in future leagues
        # structure_type: -1 = No structure, 2 = Barracks
        # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
        site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
        sites_information[site_id] = [ignore_1, ignore_2, structure_type, owner, param_1, param_2]
        temp_site_x = sites_coordinates[site_id][0]
        temp_site_y = sites_coordinates[site_id][1]
        
        distance_to_my_queen = getDistanceToMyQueenLastTurn(temp_site_x,temp_site_y)
        if structure_type == -1 and distance_to_my_queen < min_distance_to_queen:
            move_x = temp_site_x
            move_y = temp_site_y
            min_distance_to_queen = distance_to_my_queen
        if structure_type == 2 and owner == 0:
            num_of_baracks_total += 1
        
    num_units = int(input())
    for i in range(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        if unit_type == -1 and owner == 0:
            queen_x = x
            queen_y = y
            queen_health = health
            if first_round:
                if x > 1000:
                    base_x = 1920
                    base_y = 1000
        if unit_type == 1 and owner == 0:
            num_of_my_archers += 1
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # First line: A valid queen action
    # Second line: A set of training instructions
    
    if num_of_baracks_total >= len(sites_coordinates)/2:
        if queen_health < 50:
            print(f"MOVE {base_x} {base_y}")
        else:
            middle_between_archers_x = 0
            middle_between_archers_y = 0
            for archer_site in sites_with_baracks_archer:
                middle_between_archers_x += sites_coordinates[archer_site][0]
                middle_between_archers_y += sites_coordinates[archer_site][1]
            middle_between_archers_x = int(middle_between_archers_x/len(sites_with_baracks_archer))
            middle_between_archers_y = int(middle_between_archers_y/len(sites_with_baracks_archer))
            print(f"MOVE {middle_between_archers_x} {middle_between_archers_y}")
    else:
        if touched_site != -1 and sites_information[touched_site][2] == -1 and len(sites_with_baracks_archer) < 1:
            print(f"BUILD {touched_site} BARRACKS-ARCHER")
            sites_with_baracks_archer.append(touched_site)
        elif touched_site != -1 and sites_information[touched_site][2] == -1:
            print(f"BUILD {touched_site} BARRACKS-KNIGHT")
            sites_with_baracks_knights.append(touched_site)
        elif num_of_baracks_total < len(sites_coordinates)/2:
            print(f"MOVE {move_x} {move_y}")

    train_string = ""
    if num_of_my_archers < 2:
        for site_with_barack_archer in sites_with_baracks_archer:
            if gold > 100:
                train_string += f" {site_with_barack_archer}"
                gold -= 100
    if gold > 160:
        for site_with_barack_knight in reversed(sites_with_baracks_knights):
            if gold > 80:
                train_string += f" {site_with_barack_knight}"
                gold -= 80
    print(f"TRAIN{train_string}")

    num_of_baracks_total = 0
    num_of_my_archers = 0