import random
from turtle import pos, position

from sqlalchemy import true

def get_new_position(position,move_str,game_board):
    move = convert_move_str_to_object(move_str)
    move['x']+= position['x']
    move['y']+= position['y']

    if(move['x'] != position['x']):
        is_in_board(move['x'], len(game_board[0]))
    else:
        is_in_board(move['y'], len(game_board))

    return move

def update_board(position, game_board,player):

    board_value = game_board[position['y']][position['x']]
    
    if is_empty_position(board_value):
        game_board[position['y']][position['x']] = player
    elif not is_occupied_by_current_player(board_value, player):
        raise Exception("This position is occupied by this opponent")

    return game_board

def is_in_board(position,board_size):
    if position < 0 or position >= board_size:
        raise Exception("Move out of board")

def is_empty_position(position_value):
    return position_value == 0   

def is_occupied_by_current_player(position_value,player):
    return position_value == player         

def random_move():
    moves = ['up','down','left','right']
    move = random.choice(moves)
    return move

def convert_move_str_to_object(move):
    position = {'x':0,'y':0}
    if move == 'up':
        position['y'] = 1
    elif move == 'down':
        position['y'] = -1
    elif move == 'left':
        position['x'] = -1
    elif move == 'right':
        position['x'] = 1
    else :
        raise Exception("Unknown move")
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
    print(position)
    # 1 new position
    new_position = get_new_position(position,move,board_list)
    # 2 update board
    board_list = update_board(new_position,board_list,player)
    # 3 enclos
    # 4 game finish
    is_finished = is_game_finished(board_list)

    return new_position,parser_string(board_list),is_finished
    # is_valid,new_position = valid_move(position,move,board_list,player)
    # captured_positions = []
    # if is_valid:
    #     print(new_position['y'])
    #     board_list[new_position['y']][new_position['x']] = player
    #     captured_positions = enclosure(new_position,board_list)
    #     for i in range(len(captured_positions)):
    #         board[captured_positions[i]['y']][captured_positions[i]['x']] = player
    # else:
    #     return False,parser_string(board_list),[],new_position
    # return True,parser_string(board_list),captured_positions,new_position
    
def is_game_finished(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return False
    return True

