import random
from .business import *
from .models import *

import ast

import time
LEARNING_RATE = 0.1
GAMMA = 0.7
actions = ['up','down','left','right']

def train_ai(ws,nb_games = 10000):
    """
    Train the AI
    """
    p1 = Player.query.get('AI1')
    p2 = Player.query.get('AI2')
    
    for game_number in range(nb_games):
        game = Game(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1.user_name,p2.user_name,{'x':0,'y':4},{'x':4,'y':0},2)
        db.session.add(game)
        db.session.commit()
        is_finished = False
        #timer 
        start_time = time.time()
        while not is_finished:
            new_position,new_board,is_finished = step(game.board,game.current_player,ast.literal_eval(game.player_1_pos),ast.literal_eval(game.player_2_pos),0.7,is_finished)
            game.board = new_board
            if game.current_player == 1:
                game.player_1_pos = str(new_position)
            else:
                game.player_2_pos = str(new_position)
            game.current_player = 2 if game.current_player == 1 else 1
        

            
        #end timer
        ws.send("Add a game")
        print("--- %s seconds ---" % (time.time() - start_time) + " game number : " + str(game_number))





def step(board,player,player_1_pos,player_2_pos,eps,is_finished):
    new_board = board
    new_position = player_1_pos if player == 1 else player_2_pos
    player_pos = new_position
    move_not_valid = set()
    move_not_valid_enemy = set()
    move = ""
    captured_position = []
    winner = 0
    q_table_old = q_table_old = get_q_table(board, player_1_pos, player_2_pos, player)
    new_position_enemy ,new_board_best ,captured_position_ennemy ,is_finished_fac, = ((player_1_pos if player == 2 else player_2_pos),board,[],False)
    while new_position == player_pos and not is_finished:
        try:

            if len(move_not_valid) >= 1:
                move = take_action(board,player_1_pos,player_2_pos,player,0.0)
            else:
                move = take_action(board,player_1_pos,player_2_pos,player,eps)
            new_position,new_board,captured_position,is_finished,winner  = handle_move(actions[move],player_1_pos if player == 1 else player_2_pos,board,player)
            
            
            if player == 1 : player_1_pos = new_position
            else : player_2_pos = new_position

            
        except Exception as err:
            move_not_valid.add(move)

        move_ennemy = 0
        is_valid = False
        while not is_valid:
            
            try:
                if len(move_not_valid_enemy) >= 1:
                    move_ennemy = take_action(new_board,player_1_pos,player_2_pos,1 if player == 2 else 2,0.0)
                else:
                    move_ennemy = take_action(new_board,player_1_pos,player_2_pos,1 if player == 2 else 2,1.0)
                new_position_enemy ,new_board_best ,captured_position_ennemy ,is_finished_fac,winner_ennemy = handle_move(actions[move_ennemy],player_1_pos if player == 2 else player_2_pos,new_board,1 if player == 2 else 2)
                is_valid = True
            except Exception as err:                
                move_not_valid_enemy.add(move_ennemy)
   

            reward_max= 0
            if not is_finished_fac:
                q_table_new = get_q_table(new_board_best, player_1_pos if player ==1 else new_position_enemy, player_2_pos if player == 2 else new_position_enemy, player)
                reward_max = q_table_new.get_max_expected_reward()
            reward = 0

            nb_cases_captured = len(captured_position)
            if nb_cases_captured == 1:
                reward = 1.5
            if nb_cases_captured >= 2:
                reward *= nb_cases_captured * 1.5
            
            nb_cases_captured_ennemy = len(captured_position_ennemy)
            if nb_cases_captured_ennemy == 1:
                reward -= 0.5
            if nb_cases_captured_ennemy >= 2:
                reward -= nb_cases_captured_ennemy


            if winner != 0:
                if winner == player: reward += 15
                else : reward -= 20
                
            update_q_table(q_table_old,move,reward,reward_max)



    return new_position,new_board,is_finished

def update_q_table(q_table_old,action,reward,reward_max_new_state):
    q_values = q_table_old.Q_values()
    q_value = q_values[action]
    q_value += LEARNING_RATE * (reward + GAMMA * reward_max_new_state - q_value)
    if action == 1 : q_table_old.q_up = q_value
    elif action == 2 : q_table_old.q_down = q_value
    elif action == 3 : q_table_old.q_left = q_value
    else: q_table_old.q_right = q_value
    db.session.commit()

def take_action(board,player_1_pos,player_2_pos,current_player,eps):
    if random.uniform(0, 1) > eps:
        return random.randint(0,3)
    else:
        q_table = get_q_table(board, player_1_pos, player_2_pos, current_player)
        return q_table.get_best_action()


def get_q_table(board,player_1_pos,player_2_pos,current_player):
    q_table = Q_table.query.get(board + str(player_1_pos) + str(player_2_pos) + str(current_player))
    if q_table is None:
        db.session.add(Q_table(board+str(player_1_pos)+str(player_2_pos)+str(current_player)))
        db.session.commit()
        return Q_table.query.get(board + str(player_1_pos) + str(player_2_pos) + str(current_player));
    
    return q_table

