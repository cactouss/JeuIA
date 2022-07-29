import random
from turtle import pos, position

from sqlalchemy import true

def get_new_position(position,move_str,game_board):
    print(move_str)
    move = convert_move_str_to_object(move_str)
    print(type(move['x']))
    #Erreur ici string indices must be integers ?
    move['x']+= position['x']
    move['y']+= position['y']

    if(move['x'] != position['x']):
        point_is_in_board(move['x'], len(game_board[0]))
    else:
        point_is_in_board(move['y'], len(game_board))

    return move

def update_board(position, game_board,player):

    board_value = game_board[position['y']][position['x']]
    
    if is_empty_position(board_value):
        game_board[position['y']][position['x']] = player
    elif not is_occupied_by_current_player(board_value, player):
        raise Exception("This position is occupied by this opponent")

    return game_board

def point_is_in_board(position,board_size):
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
        print("Error : move not recognized")
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
    # 1 new position
    new_position = get_new_position(position,move,board_list)
    # 2 update board
    board_list = update_board(new_position,board_list,player)
    # 3 enclos
    board_list, captured_positions = enclosure(board_list,player)
    # 4 game finish
    is_finished = is_game_finished(board_list)
    
    return new_position,parser_string(board_list),captured_positions,is_finished

def is_game_finished(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return False
    return True

# prend en compte les bords donc min = -1 et max = 5
def find_sommets(board,player,x,y):
    y_min = None
    x_max = None
    x_min = None

    y_max = y + 1
    while y_max < 5:
        if board[y_max][x] == player:
            break
        elif board[y_max][x] == 0:
            y_max += 1
        else:#si autre joueur
            y_max = None
            break

    if(y_max is None): return y_max,y_min,x_max,x_min 
    y_min = y - 1
    while y_min > -1:
        if board[y_min][x] == player:
            break
        elif board[y_min][x] == 0:
            y_min -= 1
        else:#si autre joueur
            y_min = None
            break

    if(y_min is None): return y_max,y_min,x_max,x_min 
    x_max = x + 1
    while x_max < 5:
        if board[y][x_max] == player:
            break
        elif board[y][x_max] == 0:
            x_max += 1
        else:#si autre joueur
            x_max = None
            break

    if(x_max is None): return y_max,y_min,x_max,x_min 
    x_min = x - 1
    while x_min > -1:
        if board[y][x_min] == player:
            break
        elif board[y][x_min] == 0:
            x_min -= 1
        else:#si autre joueur
            x_min = None
            break
    return y_max,y_min,x_max,x_min

def enclosure(board,player):
    captured_positions = []
    for y in range(len(board)):
        for x  in range(len(board[y])):
            if board[y][x] == 0 :
                y_max,y_min,x_max,x_min = find_sommets(board,player,x,y)
                if y_max is not None and y_min is not None and x_max is not None and x_min is not None:
                    board, new_captured_positions = rectangle(x_min, x_max, y_min, y_max, board, player)
                    captured_positions.extend(new_captured_positions)
    return board,captured_positions

def rectangle(x_min,x_max,y_min,y_max,board,player):
    x = x_min
    y = y_min
    copied_board = board
    captured_positions = []
    while x <= x_max:
        while y <= y_max:
            if x == x_min or x == x_max or y == y_max or y == y_min:
                if position_is_in_board(board,x,y):
                    if board[y][x] == 0:
                        new_x = x 
                        new_y = y 
                        if x == x_min : new_x -= 1
                        if x == x_max : new_x += 1
                        if y == y_min : new_y -= 1
                        if y == y_max : new_y += 1
                        is_corner = new_x != x and new_y != y
                        if not is_corner:
                            if position_is_in_board(board,new_x,new_y) and board[new_y][new_x] != player:
                                captured_positions.clear()
                                return board,captured_positions
                            else: 
                                captured_positions.append({'x':x,'y':y})

                    elif board[y][x] != player:
                        captured_positions.clear()
                        return board,captured_positions

            else:
                if board[y][x] != player and board[y][x] != 0:
                    captured_positions.clear()
                    return board,captured_positions
                else:
                    copied_board[y][x] != player
                    captured_positions.append({'x':x,'y':y})
            y+=1
        y = y_min
        x += 1
    return copied_board,captured_positions

def position_is_in_board(game_board,x,y):
    try:
        point_is_in_board(x, len(game_board[0]))
        point_is_in_board(y, len(game_board))
        return True
    except:
        return False


