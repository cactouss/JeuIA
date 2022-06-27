import random
from turtle import pos, position

from sqlalchemy import true

def valid_move(position,move_str,game_board,player):
    move = movement(move_str)
    #check if player is still in board
    if move['x'] == 0 and move['y'] == 0:
        return False,position
    if position['y']+move['y'] < 0 or position['y']+move['y'] >= len(game_board) or position['x']+move['x'] < 0 or position['x']+move['x'] >= len(game_board[0]):
        return False,position
    #check if player doesn't on top of another player
    if game_board[position['y']+move['y']][position['x']+move['x']] != 0 and game_board[position['y']+move['y']][position['x']+move['x']] != player:
        return False,position
    return True,{'y':position['y']+move['y'],'x':position['x']+move['x']}

def random_move():
    moves = ['up','down','left','right']
    move = random.choice(moves)
    return move

def movement(move):
    position = {'x':0,'y':0}
    if move == 'up':
        position['y'] = 1
    elif move == 'down':
        position['y'] = -1
    elif move == 'left':
        position['x'] = -1
    elif move == 'right':
        position['x'] = 1
    return position
        
def parser_string(board):
    res = ""
    for i in range(len(board)):
        for j in range(len(board[i])):
            res += str(board[i][j])
        res+="/"
    
    return res[:-1]

def parse_list(board_str):
    board_str = board_str.split("/")
    board = []
    for i in range(len(board_str)):
        board.append([])
        for j in range(len(board_str[i])):
            board[i].append(int(board_str[i][j]))
    return board
def enclosure(position,board):
    #dans l'idéale return la list des positions nouvellement acquises
    return []
def handle_move(move,position,board,player):
    board_list = parse_list(board)
    is_valid,new_position = valid_move(position,move,board_list,player)
    captured_positions = []
    if is_valid:
        print(new_position['y'])
        board_list[new_position['y']][new_position['x']] = player
        captured_positions = enclosure(new_position,board_list)
        for i in range(len(captured_positions)):
            board[captured_positions[i]['y']][captured_positions[i]['x']] = player
    else:
        return False,parser_string(board_list),[],new_position
    return True,parser_string(board_list),captured_positions,new_position
    
def is_game_finished(board):
    board = parse_list(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return False
    return True