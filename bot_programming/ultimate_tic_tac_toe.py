import sys
from math import inf as infinity
from random import choice
import math


PLAYER = +1
ENEMY = -1

def evaluate(board):
    if wins(board, ENEMY):
        score = +1
    elif wins(board, PLAYER):
        score = -1
    else:
        score = 0
    return score   

def wins(board, player):
    win_state = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def game_over(board):
    return wins(board, PLAYER) or wins(board, ENEMY)

def empty_cells(board):
    cells = []
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells

def turn(board, depth):
    if depth == 0 or game_over(board):
        debugprint('depth is 0')
        return (0,0)
    if depth == 9:
        debugprint('depth is 9')
        x = 1
        y = 1
    else:
        move = minimax(board, depth, PLAYER)
        x, y = move[0], move[1]
    return (x, y)

def minimax(board, depth, player):
    # if depth == 0 or game_over(board):
    if depth < 4 or game_over(board):
        score = evaluate(board)
        return [-1, -1, score]
    if player == ENEMY:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    for cell in empty_cells(board):
        x, y = cell[0], cell[1]
        board[x][y] = player
        score = minimax(board, depth - 1, -player)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == ENEMY:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def get_x(x):
    if x == 0 or x == 3 or x == 6:
        return 0
    if x == 1 or x ==4 or x == 7:
        return 1
    if x == 2 or x == 5 or x == 8:
        return 2
    return 0


def debugprint(stringtoprint):
    print(stringtoprint, file=sys.stderr, flush=True)

def get_single_board(big_board, big_board_move_given_by_enemy):
    big_board_y, big_board_x = big_board_move_given_by_enemy
    board[0][0] = big_board[big_board_y*3][big_board_x*3]
    board[0][1] = big_board[big_board_y*3][big_board_x*3+1]
    board[0][2] = big_board[big_board_y*3][big_board_x*3+2]
    board[1][0] = big_board[big_board_y*3+1][big_board_x*3]
    board[1][1] = big_board[big_board_y*3+1][big_board_x*3+1]
    board[1][2] = big_board[big_board_y*3+1][big_board_x*3+2]
    board[2][0] = big_board[big_board_y*3+2][big_board_x*3]
    board[2][1] = big_board[big_board_y*3+2][big_board_x*3+1]
    board[2][2] = big_board[big_board_y*3+2][big_board_x*3+2]
    return board

big_board = [[0]*9 for i in range(9)]
big_board_validated = [[0]*3 for i in range(3)]

# game loop
while True:
    printstring = ''
    board = [[0]*3 for i in range(3)]

    opponent_y, opponent_x = [int(i) for i in input().split()]
    big_board[opponent_y][opponent_x] = ENEMY # make enemy move in my board
    big_board_move_given_by_enemy = (0,0)
    if opponent_y != -1:
        big_board_move_given_by_enemy = (get_x(opponent_y), get_x(opponent_x))
    valid_action_count = int(input())
    for i in range(valid_action_count):
        y, x = [int(j) for j in input().split()]

    # evaluate in which small board move should be made:
    # depth = len(empty_cells(big_board_validated))
    # big_board_turn = turn(big_board_validated, depth)
    
    # get small board of coordinates
    # big_board_y,big_board_x = big_board_turn[0], big_board_turn[1]
    big_board_y, big_board_x = big_board_move_given_by_enemy    
    board = get_single_board(big_board, big_board_move_given_by_enemy)
    iterator = 1
    while game_over(board):
        big_board_move_given_by_enemy_new = (0+iterator,0)
        board = get_single_board(big_board, big_board_move_given_by_enemy_new)
        iterator += 1
        big_board_y, big_board_x = big_board_move_given_by_enemy_new    

    depth_small = len(empty_cells(board))
    turntodo = turn(board, depth_small)
    big_board[turntodo[0]+big_board_y*3][turntodo[1]+big_board_x*3] = PLAYER

    print(f"{turntodo[0]+big_board_y*3} {turntodo[1]+big_board_x*3}")
