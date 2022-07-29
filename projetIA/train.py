import random
import numpy as np
from .business import *
from .models import *
import copy
#import time
import time
LEARNING_RATE = 0.1 
GAMMA = 0.9
NB_GAEMES_EXPLORATION = 5000
actions = ['up','down','left','right']
def espylon_greedy(eps,gameId):
    return eps if gameId < NB_GAEMES_EXPLORATION else eps * 0.995

def take_action(board,player_1_pos,player_2_pos,current_player, eps):
    """
    Take an action according to the epsilon-greedy policy
    """
    if random.uniform(0, 1) < eps:
        action = random.randint(0,3)
    else:
        #TODO: Get the qTable value for the current state -> board + posPlayer1 + posPlayer2
        action = 0
    return action

def train_ai(nb_games = 1):
    global eps 
    eps = 0.9
    """
    Train the AI
    """
    actions = ['up','down','left','right']
    p1 = Player.query.get('AI1')
    p2 = Player.query.get('AI2')
    game = Game(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1.user_name,p2.user_name,str({'x':0,'y':4}),str({'x':4,'y':0}),1)
    db.session.add(game)
    db.session.commit()
    print("hey")
    for _ in range(nb_games):
        is_finished = False
        #timer 
        start_time = time.time()
        while not is_finished:
            old_board = game.board
            new_position,new_board,is_finished = step(game.board,game.current_player,game.player_1_pos if game.current_player == 1 else game.player_2_pos,0.4)
            new_position_enemy , new_boardT1,is_finished = step(game.board,2 if game.current_player == 1 else 1,game.player_2_pos if game.current_player == 1 else game.player_1_pos,0.0)
            game.board = new_board
            if game.current_player == 1:
                game.player_1_pos = new_position
            else:
                game.player_2_pos = new_position
            game.current_player = 2 if game.current_player == 1 else 1
            
        #end timer
        print("--- %s seconds ---" % (time.time() - start_time))
            
            
        game = Game(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1.user_name,p2.user_name,str({'x':0,'y':4}),str({'x':4,'y':0}),1)





def step(board,player,player_pos,eps):
    new_position = player_pos
    while new_position == player_pos:
        try:
            move = take_action(board,player_pos,player_pos,player,eps)
            
            new_position,new_board,captured_position,is_finished  = handle_move(actions[move],player_pos,board,player)
        except Exception as err:
            print("-----------------Error-----------------")
            print(err)
            print("-----------------Error-----------------")
            player_pos = new_position

    return new_position,new_board,is_finished

def take_action(board,player_1_pos,player_2_pos,current_player,eps):
    if random.uniform(0, 1) < eps:
        return random.randint(0,3)
    else:
        actions = Q_table.query.get(board + str(player_1_pos) + str(player_2_pos) + str(current_player))
        if actions is None:
            db.session.add(Q_table(board+str(player_1_pos)+str(player_2_pos)+str(current_player)))
            db.session.commit()
            return random.randint(0,3)
        else:
            return np.max(actions.Q_values())

























#     state = game.board + str(game.player_1_pos) + str(game.player_2_pos) + str(game.current_player)
#     actions= ['up','down','left','right']
#     for i in range(nb_games):
#         is_finished = False
#         while not is_finished:
            
            
#             db.session.add(game)
#             nb_turn = 0
#             eps = espylon_greedy(eps,game.id)
#             while not is_finished:
#                 #player 1 move and update q tabkle
#                 try:
#                     action = take_action(game.board,game.player_1_pos,game.player_2_pos,1,eps)
#                     new_board, new_player_pos_P1 = take_step(game.board,game.player_1_pos,1,actions[action])
#                 except Exception as e:
#                     #handle game finished
#                     break
#                 try:
#                     action_p2 = take_action(new_board,new_player_pos_P1,game.player_2_pos,2,0.0)
#                     new_board_p2, new_player_pos_p2 = take_step(new_board,game.player_2_pos,2,actions[action_p2])
#                 except Exception as e:
#                     #handle if game should be finished
#                     print("")
#                 action_p1_1 = take_action(new_board_p2,new_player_pos_p2,new_player_pos_P1,1,0.00)
#                 #calculate reward and update q table
#                 game.board = new_board
#                 game.player1_pos = new_player_pos_P1
#                 game.current_player = 2

#                 #player 2 move and update q table
#                 try:
#                     action = take_action(game.board,game.player_1_pos,game.player_2_pos,2,eps)
#                     new_board, new_player_pos_P2 = take_step(game.board,game.player_2_pos,2,actions[action])
#                 except Exception as e:
#                     #handle game finished
#                     break
#                 try:
#                     action_p1 = take_action(new_board,new_player_pos_P2,game.player_1_pos,1,0.0)
#                     new_board_p1, new_player_pos_p1 = take_step(new_board,game.player_1_pos,1,actions[action_p2])
#                 except Exception as e:
#                     #handle if game should be finished
#                     print("")
#                 action_p1_1 = take_action(new_board_p1,new_player_pos_p2,new_player_pos_P1,2,0.0)
#                 game.board = new_board
#                 game.player2_pos = new_player_pos_P2
#                 game.current_player = 1
#                 nb_turn += 1
#                 #calculate reward and update q table 
#         game.__init__(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1,p2,{'x':0,'y':4},{'x':4,'y':0},1) #reset game

                


                    

#         eps = espylon_greedy(eps,game.id)

#         print(f"training at game{(i+1/nb_games)*100} % ")
    


            
            
# def take_step(board,current_player_pos,current_player,action):
#     """
#     Take a step in the game
#     """
#     old_player_pos = copy.copy(current_player_pos)
#     old_board = copy.copy(board)
#     new_player_pos = copy.copy(old_player_pos)
#     while old_player_pos == new_player_pos:
#         new_player_pos,new_board,captured_positions,is_finished = handle_move(actions[action],old_player_pos,old_board,current_player)
#     if is_finished:
#         raise Exception("Game finished")
#     return new_board, new_player_pos



# def calculate_reward(old_board,new_board, player):
#     """
#     Calculate the reward for the current state
#     """
#     return 0
    


