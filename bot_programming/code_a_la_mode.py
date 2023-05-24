import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

printstring = ""

current_command = ''
myplayer = ()
moveabletiles = []
countertiles = []

def move_to(coordinates):
    global printstring
    printstring = f"MOVE {coordinates[0]} {coordinates[1]}"

def use_thing(coordinates):
    global printstring
    printstring = f"USE {coordinates[0]} {coordinates[1]}"

def debugprint(toprint):
    print(toprint, file=sys.stderr, flush=True)

def get_closest_tile(goalstring):
    closest_moveable_tile = ()
    closest_current_distance = 100
    goal_coordinates = kitchenmap[goalstring]
    for tile in moveabletiles:
        if get_distance_between_points(tile, goal_coordinates) < closest_current_distance:
            closest_moveable_tile = tile
    return closest_moveable_tile

def get_closest_counter_tile():
    closest_counter_tile = ()
    closest_current_distance = 100
    goal_coordinates = myplayer
    for tile in countertiles:
        if get_distance_between_points(tile, goal_coordinates) < closest_current_distance:
            closest_counter_tile = tile
    return closest_counter_tile

def get_distance_between_points(pointa, pointb):
    first = (pointb[0] - pointa[0]) ** 2   
    second = (pointb[1] - pointa[1]) ** 2
    return math.sqrt(first+second)

def split_order_into_array(orderstring):
    orderarray = orderstring.split('-')
    orderarray = orderarray[::-1]
    debugprint(orderarray)
    # for i in range(len(orderarray)):
    #     orderarray[i] = orderarray[i][0]
    # debugprint(orderarray)
    return orderarray

def put_hands_on_closest_counter():
    closest_counter_tile_coordinates = get_closest_counter_tile()
    use_thing(closest_counter_tile_coordinates)


chopped_strawberries = []
def prepareorder(ordername, playeritem):
    global current_command
    global chopped_strawberries
    ingredientarray = split_order_into_array(ordername)
    playeritemarray = split_order_into_array(playeritem)
    debugprint(ingredientarray)
    debugprint(playeritemarray)
    while len(ingredientarray) > 0:
        current_command = ingredientarray[-1]
        debugprint('currentcommand = ' + current_command)
        if chopped_strawberries and ingredientarray[-1] == 'STRAWBERRIES':
            ingredientarray.pop()
            ingredientarray.pop()
            # todo emptyhands
            put_hands_on_closest_counter()
            continue


        if len(playeritemarray) != 0:
            if playeritemarray[-1] == current_command:
                playeritemarray.pop()
                ingredientarray.pop()
                debugprint(f'player already has {current_command}')
                continue
            if playeritemarray[-1] == 'CHOPPED_STRAWBERRIES':
                # player has chopped strawberries in hand
                put_hands_on_closest_counter()
                break
        debugprint(current_command)
        if current_command == 'CHOPPED_STRAWBERRIES' and playeritemarray[-1] == "STRAWBERRIES": #chopped strawberries    
            strawberries_coordinates = chopped_strawberries.pop()
            if command_in_reach(strawberries_coordinates):
                use_thing(strawberries_coordinates)
                break
            else:    
                move_to(strawberries_coordinates)
                break
        if command_in_reach(kitchenmap[current_command]):
            use_thing(kitchenmap[current_command])
            break
        else:    
            move_to(kitchenmap[current_command])
            break
    debugprint(playeritemarray)
    debugprint(ingredientarray)
    if playeritemarray == ingredientarray:
        debugprint('turning in')
        if command_in_reach(kitchenmap['W']):
            use_thing(kitchenmap['W'])
        else:
            move_to(kitchenmap['W'])


def command_in_reach(command_coordinates):
    distance_to_command = get_distance_between_points(command_coordinates, myplayer)
    debugprint(distance_to_command)
    return distance_to_command < 1.5

# todo later
def get_order_prio_map(orderlist):
    order_prio_map = {1: (), 2:(), 3:()}
    for index, order in enumerate(orderlist):
        order_prio_map[index] = order
    return order_prio_map


orderlist = [] # tuple


kitchenmap = {}
num_all_customers = int(input())
for i in range(num_all_customers):
    inputs = input().split()
    customer_item = inputs[0]  # the food the customer is waiting for
    customer_award = int(inputs[1])  # the number of points awarded for delivering the food
    orderlist.append((customer_item, customer_award))
for i in range(7):
    kitchen_line = input()
    column = 0
    for j in range(len(kitchen_line)):
        if kitchen_line[j] == "D":
            kitchenmap["DISH"] = (column, i)
        elif kitchen_line[j] == "W":
            kitchenmap[kitchen_line[j]] = (column, i)
        elif kitchen_line[j] == "B":
            kitchenmap["BLUEBERRIES"] = (column, i)
        elif kitchen_line[j] == "I":
            kitchenmap["ICE_CREAM"] = (column, i)
        elif kitchen_line[j] == "S":
            kitchenmap["STRAWBERRIES"] = (column, i)
        elif kitchen_line[j] == "C":
            kitchenmap[kitchen_line[j]] = (column, i)
        elif kitchen_line[j] == "." or kitchen_line[j] == "0" or kitchen_line[j] == "1":
            moveabletiles.append((column, i))
        else:
            countertiles.append((column, i))
        column+=1



debugprint('kitchenmap')
debugprint(kitchenmap)
    
playeritem = ''

# game loop
while True:
    
    turns_remaining = int(input())
    inputs = input().split()
    player_x = int(inputs[0])
    player_y = int(inputs[1])
    myplayer = (player_x, player_y)
    player_item = inputs[2]
    playeritem = player_item
    inputs = input().split()
    partner_x = int(inputs[0])
    partner_y = int(inputs[1])
    partner_item = inputs[2]
    num_tables_with_items = int(input())  # the number of tables in the kitchen that currently hold an item
    for i in range(num_tables_with_items):
        inputs = input().split()
        table_x = int(inputs[0])
        table_y = int(inputs[1])
        item = inputs[2]
        if item == "CHOPPED_STRAWBERRIES":
            chopped_strawberries.append((table_x,table_y))
    inputs = input().split()
    oven_contents = inputs[0]  # ignore until wood 1 league
    oven_timer = int(inputs[1])
    num_customers = int(input())  # the number of customers currently waiting for food
    for i in range(num_customers):
        inputs = input().split()
        customer_item = inputs[0]
        customer_award = int(inputs[1])
        if "STRAWBERRIES" in customer_item:
            customer_item = "STRAWBERRIES-CHOPPED_STRAWBERRIES-" + customer_item
        orderlist.append((customer_item, customer_award))

    order_prio_map = get_order_prio_map(orderlist)
    prepareorder(order_prio_map[1][0], playeritem)


    print(printstring)

    orderlist = []
    myplayer = ()