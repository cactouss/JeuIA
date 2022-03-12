import random

def valid_move(position,move,game_board,player):
#position {x y} -> correspondant a la position du joueur dans la matrice game board
#move {x y }
    mouvement(move['x'], move['y'])
    if (move['x'] == 0 and move['y'] == 0) or (move['x'] != 0 and move['y'] != 0) or (move['x'] > 1 or move['x'] < -1 or move['y'] > 1 or move['y'] < -1):
        return False,position
    
    min = 0
    max = 4

    new_position = {'x': position['x'] + move['x'], 'y': position['y'] + move['y']}
    if new_position['y'] < min or new_position['y'] > max or new_position['x'] > max or new_position['x'] < min:
        return False,position
    if game_board[new_position['x']][new_position['y']] == 0 or game_board[new_position['x']][new_position['y']] == player :
        return True,new_position
    return False,position

def random_move(position,game_board,player):
    is_valid_move = False
    while(not is_valid_move):
        x = random.randint(-1,1)
        y = random.randint(-1,1)
        is_valid_move, position = valid_move(position,{'x':x, 'y':y},game_board,player)
    return position

def mouvement(x,y):
    if x == 0 and y == -1:
        print("up")
    elif x == 0 and y == 1:
        print("down")
    elif x == 1 and y == 0:
        print("right")
    elif x == -1 and y == 0:
        print("left")
    else:
        print(f'Move non valide x:{x} y:{y}')
