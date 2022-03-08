def valid_move(position,move,game_board,player):
#position {x y} -> correspondant a la position du joueur dans la matrice game board
#move {x y }
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