import copy
import sys

width, height = [int(i) for i in input().split()]
commandstring = ""
my_tiles_dict = {}
all_tiles_dict = {}
enemy_tiles_dict = {}
tiles_to_take_dict = {}
neutral_tiles_dict = {}
tiles_to_take_list = []
tiles_to_take_with_range_dict = {}
my_robots_dict = {}
my_robots_list = []
enemy_robots_dict = {}
no_move_tiles = []
limited_move_robots = {}
no_move_robots = []
matter_used_this_turn = 0
safing_matter = 0
random_spawn_tile = ()
enemy_border_tiles = set()
my_border_tiles = set()

my_side_is_left = True
my_side_set = False

enemy_surrounded_by_grass = True
grid = [[0 for x in range(height)] for y in range(width)]
y_value_taken = set()

### functions ###


def move_command(units, robot_coordinates, move_to_coordinates):
    return f"MOVE {units} {robot_coordinates[0]} {robot_coordinates[1]} {move_to_coordinates[0]} {move_to_coordinates[1]};"


def spawn_command(units, coordinates):
    return f"SPAWN {units} {coordinates[0]} {coordinates[1]};"


def build_command(coordinates):
    return f"BUILD {coordinates[0]} {coordinates[1]};"


def debug(message):
    print(message, file=sys.stderr, flush=True)

# -- calculations -- #


def get_distance_between(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])

def get_x_y_distance_between(point_a, point_b):
    return (abs(point_a[0] - point_b[0]), abs(point_a[1] - point_b[1]))

def enough_matter_available(wished_matter_used, my_current_matter, my_matter_used_this_turn):
    return (my_current_matter - my_matter_used_this_turn) - wished_matter_used >= safing_matter


def can_spawn_to_defend(my_matter, matter_used_this_turn, my_robot_count, enemy_robot_count):
    can_spawn = False
    if ((enemy_robot_count - my_robot_count) + 1) * 10 < my_matter - (matter_used_this_turn - safing_matter):
        can_spawn = True
    return can_spawn, (enemy_robot_count - my_robot_count) + 1


def get_new_tile_values_change_units(units_to_spawn, values):
    scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = values
    units = units + units_to_spawn
    return scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler


def get_nearest_enemy_border_tile(enemy_border_tiles_for_loop, my_robot_coordinate):
    nearest_enemy_tile = (1000, 1000)
    current_shortest_distance = 1000
    for enemy_border_tile in enemy_border_tiles_for_loop:
        distance = get_distance_between(my_robot_coordinate, enemy_border_tile)
        if distance < current_shortest_distance:
            nearest_enemy_tile = enemy_border_tile
            current_shortest_distance = distance
    return nearest_enemy_tile


def get_nearest_my_border_tile(my_border_tiles_for_loop, my_robot_coordinate):
    nearest_my_tile = (1000, 1000)
    current_shortest_distance = 1000
    for my_border_tile in my_border_tiles_for_loop:
        distance = get_distance_between(my_robot_coordinate, my_border_tile)
        if distance < current_shortest_distance:
            nearest_my_tile = my_border_tile
            current_shortest_distance = distance
    return nearest_my_tile

def get_nearest_object_x_y_focus(to_loop, distance_to_object):
    nearest_object = (1000, 1000)
    current_y_diff = 1000
    current_x_diff = 1000
    for loop_coordinates in to_loop:
        distance = get_x_y_distance_between(distance_to_object, loop_coordinates)
        if distance[1] < current_y_diff: # y is smaller than current y -> pref
            if distance[0] <= current_x_diff or distance[0] <= current_y_diff:
                nearest_object = loop_coordinates
                current_x_diff = distance[0]
                current_y_diff = distance[1]
        elif distance[1] == current_y_diff:
            if distance[0] < current_x_diff:
                nearest_object = loop_coordinates
                current_x_diff = distance[0]
                current_y_diff = distance[1]
        else: # y diff is bigger than before
            if distance[0] < current_x_diff:
                nearest_object = loop_coordinates
                current_x_diff = distance[0]
                current_y_diff = distance[1]
    return nearest_object

def get_nearest_object_x_y_focus_robots(to_loop, distance_to_object, no_move_robots):
    nearest_object = (1000, 1000)
    current_y_diff = 1000
    current_x_diff = 1000
    for loop_coordinates in to_loop:
        if loop_coordinates not in no_move_robots:
            distance = get_x_y_distance_between(distance_to_object, loop_coordinates)
            if distance[1] < current_y_diff: # y is smaller than current y -> pref
                if distance[0] <= current_x_diff or distance[0] <= current_y_diff:
                    nearest_object = loop_coordinates
                    current_x_diff = distance[0]
                    current_y_diff = distance[1]
            elif distance[1] == current_y_diff:
                if distance[0] < current_x_diff:
                    nearest_object = loop_coordinates
                    current_x_diff = distance[0]
                    current_y_diff = distance[1]
            else: # y diff is bigger than before
                if distance[0] < current_x_diff:
                    nearest_object = loop_coordinates
                    current_x_diff = distance[0]
                    current_y_diff = distance[1]
    return nearest_object

# -- calculations -- #

### functions ###

### Objects ###


class Cell:
    def __init__(self, scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler):
        self.scrap_amount = scrap_amount
        self.owner = owner
        self.units = units
        self.recycler = recycler
        self.can_build = can_build
        self.can_spawn = can_spawn
        self.in_range_of_recycler = in_range_of_recycler
### Objects ###


while True:
    my_matter, opp_matter = [int(i) for i in input().split()]
    for y in range(height):
        for x in range(width):
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [
                int(k) for k in input().split()]
        ### grid ###
            grid[x][y] = Cell(scrap_amount, owner, units, recycler,
                              can_build, can_spawn, in_range_of_recycler)
        ### grid ###

        ### all ###
            all_tiles_dict[(
                x, y)] = scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler
        ### neutral ###
            if owner == -1 and scrap_amount > 0:
                neutral_tiles_dict[(
                    x, y)] = scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler

        ### me ###
            if owner == 1:
                my_tiles_dict[(
                    x, y)] = scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler
                random_spawn_tile = (x, y)
                if units > 0:
                    my_robots_dict[(x, y)] = units
                    my_robots_list.append((x,y))
        ### enemy ###
            if owner == 0:
                if not my_side_set and x < width/2:
                    my_side_is_left = False
                    my_side_set = True
                enemy_tiles_dict[(
                    x, y)] = scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler
                if units > 0:
                    enemy_robots_dict[(x, y)] = units
        # tiles that can be taken next turn
            if owner != 1 and scrap_amount > 0 and not (scrap_amount == 1 and in_range_of_recycler == 1):
                tiles_to_take_list.append((x, y))
                tiles_to_take_dict[(
                    x, y)] = scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler

    # for y in range(height):
    #     for x in range(width):
    #         debug(f"{x}:{y}")
    #         debug(f"scrapvalue {grid[x][y].scrap_amount}")

##### MY BORDER TILES  #####
    for my_coordinate in my_tiles_dict.keys():
        x_plus_one = (my_coordinate[0] + 1, my_coordinate[1])
        x_minus_one = (my_coordinate[0] - 1, my_coordinate[1])
        y_plus_one = (my_coordinate[0], my_coordinate[1] + 1)
        y_minus_one = (my_coordinate[0], my_coordinate[1] - 1)
        coordinates_to_check = [x_plus_one,
                                x_minus_one, y_plus_one, y_minus_one]
        if my_side_is_left:
            coordinates_to_check.remove(x_minus_one)
        else:
            coordinates_to_check.remove(x_plus_one)
        for coordinate in coordinates_to_check:
            ## ** check neighboring cells if they are neutral and takeable ** ##
            if coordinate in tiles_to_take_dict.keys():
                tile_to_add = ()
                if my_side_is_left:
                    for i in range(coordinate[0] + 1, width):
                        if (i, coordinate[1]) in my_border_tiles:
                            if (i - 1, coordinate[1]) in my_border_tiles:
                                my_border_tiles.remove(
                                    (i - 1, coordinate[1]))
                            tile_to_add = ((i, coordinate[1]))
                    if not tile_to_add:
                        my_border_tiles.add(coordinate)
                    else:
                        my_border_tiles.add(tile_to_add)
                else:  # my side is right
                    for i in range(coordinate[0] + 1, 0, -1):
                        if (i, coordinate[1]) in my_border_tiles:
                            if (i + 1, coordinate[1]) in my_border_tiles:
                                my_border_tiles.remove(
                                    (i + 1, coordinate[1]))
                            tile_to_add = ((i, coordinate[1]))
                    if not tile_to_add:
                        my_border_tiles.add(coordinate)
                    else:
                        my_border_tiles.add(tile_to_add)

##### MY BORDER TILES  #####

#### ENEMY BORDER TILES #####
    for enemy_coordinate in enemy_tiles_dict.keys():
        x_plus_one = (enemy_coordinate[0] + 1, enemy_coordinate[1])
        x_minus_one = (enemy_coordinate[0] - 1, enemy_coordinate[1])
        y_plus_one = (enemy_coordinate[0], enemy_coordinate[1] + 1)
        y_minus_one = (enemy_coordinate[0], enemy_coordinate[1] - 1)
        coordinates_to_check = [x_plus_one,
                                x_minus_one, y_plus_one, y_minus_one]
        for coordinate in coordinates_to_check:
            if coordinate in all_tiles_dict:
                if all_tiles_dict[coordinate][0] > 0 and all_tiles_dict[coordinate][1] != 0:
                    enemy_surrounded_by_grass = False


###################  DEFENDING TILE #########################
    ### BLOCK ENEMIES OR SPAWN ROBOTS ###
    for enemy_coordinate in enemy_robots_dict.keys():
        x_plus_one = (enemy_coordinate[0] + 1, enemy_coordinate[1])
        x_minus_one = (enemy_coordinate[0] - 1, enemy_coordinate[1])
        y_plus_one = (enemy_coordinate[0], enemy_coordinate[1] + 1)
        y_minus_one = (enemy_coordinate[0], enemy_coordinate[1] - 1)
        coordinates_to_check = [x_plus_one,
                                x_minus_one, y_plus_one, y_minus_one]
        for coordinate in coordinates_to_check:
            ## check spawning or building ##
            # neighbor = mine and no recycler
            if coordinate in my_tiles_dict.keys() and my_tiles_dict[coordinate][3] == 0:
                # my units -> no building possible
                if my_tiles_dict[coordinate][2] != 0:
                    # me more than him
                    if my_tiles_dict[coordinate][2] > enemy_tiles_dict[enemy_coordinate][2]:
                        units_to_move = my_tiles_dict[coordinate][2] - \
                            enemy_tiles_dict[enemy_coordinate][2]
                        limited_move_robots[my_tiles_dict[coordinate]
                                            ] = units_to_move
                        new_values = get_new_tile_values_change_units(
                            -units_to_move, my_tiles_dict[coordinate])
                        my_tiles_dict[coordinate] = new_values
                    elif my_tiles_dict[coordinate][2] < enemy_tiles_dict[enemy_coordinate][2]:
                        spawn_to_defend, units_to_spawn = can_spawn_to_defend(
                            my_matter, matter_used_this_turn, my_tiles_dict[coordinate][2], enemy_tiles_dict[enemy_coordinate][2])
                        if spawn_to_defend:
                            commandstring += spawn_command(
                                units_to_spawn, coordinate)
                            new_values = get_new_tile_values_change_units(
                                units_to_spawn, my_tiles_dict[coordinate])
                            my_tiles_dict[coordinate] = new_values
                            matter_used_this_turn += 10 * units_to_spawn
                    elif my_tiles_dict[coordinate][2] == enemy_tiles_dict[enemy_coordinate][2]:
                        # BUG: sets it on no move list before checking other tiles around
                        no_move_robots.append(coordinate)
                else:  # no units -> building possible
                    if coordinate in all_tiles_dict.keys() and all_tiles_dict[coordinate][0] > 0:
                        enemy_surrounded_by_grass = False
                    if enough_matter_available(10, my_matter, matter_used_this_turn):
                        commandstring += build_command(coordinate)
                        matter_used_this_turn += 10
                        no_move_tiles.append(coordinate)
            ## ##
    ### END BLOCK ENEMIES ###
###################  END BUILDING #########################
###################  SPAWNING #########################
    for my_tile in my_tiles_dict.keys():
        if enough_matter_available(10, my_matter, matter_used_this_turn):
            commandstring += spawn_command(1, my_tile)
            matter_used_this_turn += 10
###################  END SPAWNING #########################
###################  MOVING #########################
    spread_out = False
    if enemy_surrounded_by_grass == True:  # fill everything
        debug("enemy surrounded")
        for my_robot_coordinates, my_robot_units in my_robots_dict.items():
            tile_coordinates = (1000, 1000)
            shortest_distance = 1000
            for empty_tile in neutral_tiles_dict.keys():
                current_distance = get_distance_between(
                    my_robot_coordinates, empty_tile)
                if current_distance < shortest_distance:
                    shortest_distance = current_distance
                    tile_coordinates = empty_tile
            if tile_coordinates != (1000, 1000):
                commandstring += move_command(my_robot_units,
                                              my_robot_coordinates, tile_coordinates)
            else:
                commandstring = "WAIT;"
                commandstring += "MESSAGE \\O/;"
    else:
        if spread_out:
            my_border_tiles_for_loop = copy.deepcopy(my_border_tiles)
            for my_tile_coordinate in my_border_tiles_for_loop:
                if len(no_move_robots) != len(my_robots_dict):
                    if len(my_border_tiles) > len(my_robots_list):
                        debug("not enough robots to cover border") 
                    nearest_robot = get_nearest_object_x_y_focus_robots(
                            my_robots_list, my_tile_coordinate, no_move_robots)
                    move_amount = my_robots_dict[nearest_robot]
                    if nearest_robot in limited_move_robots:
                        move_amount = limited_move_robots[nearest_robot]
                    commandstring += move_command(move_amount,
                                                    nearest_robot, my_tile_coordinate)
                    no_move_robots.append(nearest_robot)
                    # my_robots_list.remove[nearest_robot]
        else:
            my_border_tiles_for_loop = copy.deepcopy(my_border_tiles)
            for my_robot_coordinate, my_robot_units in my_robots_dict.items():
                if my_robot_coordinate not in no_move_robots:
                    move_amount = my_robot_units
                    if my_robot_coordinate in limited_move_robots:
                        move_amount = limited_move_robots[my_robot_coordinate]
                    if len(my_border_tiles_for_loop) == 0:
                        my_border_tiles_for_loop = copy.deepcopy(my_border_tiles)

                    nearest_my_tile = get_nearest_object_x_y_focus(
                        my_border_tiles_for_loop, my_robot_coordinate)
                    if nearest_my_tile == (1000, 1000):
                        my_border_tiles_for_loop = my_border_tiles
                        nearest_my_tile = get_nearest_object_x_y_focus(
                            my_border_tiles_for_loop, my_robot_coordinate)
                        commandstring += move_command(move_amount,
                                                    my_robot_coordinate, nearest_my_tile)
                    else:
                        my_border_tiles_for_loop.remove(nearest_my_tile)
                        commandstring += move_command(move_amount,
                                                    my_robot_coordinate, nearest_my_tile)

    # else:
    #     enemy_border_tiles_for_loop = enemy_border_tiles

    #     for my_robot_coordinate in my_robots_dict.keys():
    #         nearest_enemy_tile = get_nearest_enemy_border_tile(enemy_border_tiles_for_loop, my_robot_coordinate)
    #         if nearest_enemy_tile == (1000, 1000):
    #             enemy_border_tiles_for_loop = enemy_border_tiles
    #             nearest_enemy_tile = get_nearest_enemy_border_tile(enemy_border_tiles_for_loop, my_robot_coordinate)
    #             commandstring += move_command(1, my_robot_coordinate, nearest_enemy_tile)
    #         else:
    #             enemy_border_tiles_for_loop.remove(nearest_enemy_tile)
    #             commandstring += move_command(1, my_robot_coordinate, nearest_enemy_tile)

###################  END MOVING #########################
###################  PRINTING #########################
    print("WAIT") if len(commandstring) == 0 else print(commandstring)
###################  PRINTING END #########################

###################  RESETTING #########################
    commandstring = ""
    my_tiles_dict = {}
    all_tiles_dict = {}
    enemy_tiles_dict = {}
    neutral_tiles_dict = {}
    tiles_to_take_list = []
    tiles_to_take_with_range_dict = {}
    my_robots_dict = {}
    enemy_robots_dict = {}
    my_robots_list = []
    no_move_tiles = []
    limited_move_robots = {}
    no_move_robots = []
    matter_used_this_turn = 0
    safing_matter = 0
    random_spawn_tile = ()
    enemy_border_tiles = set()
    my_border_tiles = set()
    enemy_surrounded_by_grass = True
    tiles_to_take_dict = {}


###################  END RESETTING #########################
