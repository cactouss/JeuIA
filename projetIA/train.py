import random
from requests import session
from .business import *
from .models import *
import copy
import ast
#import time
import time

NB_GAEMES_EXPLORATION = 5000
actions = ['up','down','left','right']
def espylon_greedy(eps,gameId):
    return eps if gameId < NB_GAEMES_EXPLORATION else eps * 0.995

# def take_action(board,player_1_pos,player_2_pos,current_player, eps):
#     """
#     Take an action according to the epsilon-greedy policy
#     """
#     if random.uniform(0, 1) < eps:
#         action = random.randint(0,3)
#     else:
        
#         #TODO: Get the qTable value for the current state -> board + posPlayer1 + posPlayer2
#         action = 0
#     return action

def train_ai(nb_games = 10):
    global eps 
    eps = 0.9
    """
    Train the AI
    """
    actions = ['up','down','left','right']
    p1 = Player.query.get('AI1')
    p2 = Player.query.get('AI2')
    game = Game(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1.user_name,p2.user_name,{'x':0,'y':4},{'x':4,'y':0},1)
    db.session.add(game)
    db.session.commit()
    nb_move = 0
    for _ in range(nb_games):
        is_finished = False
        #timer 
        start_time = time.time()
        while not is_finished:
            old_board = game.board
            new_position,new_board,is_finished = step(game.board,game.current_player,ast.literal_eval(game.player_1_pos),ast.literal_eval(game.player_2_pos),0.4,is_finished)
            new_position_enemy , new_boardT1,is_finished = step(game.board,2 if game.current_player == 1 else 1,ast.literal_eval(game.player_1_pos),ast.literal_eval(game.player_2_pos),0.0,is_finished)
            game.board = new_board
            if game.current_player == 1:
                game.player_1_pos = str(new_position)
            else:
                game.player_2_pos = str(new_position)
            game.current_player = 2 if game.current_player == 1 else 1


            
        #end timer
        print("--- %s seconds ---" % (time.time() - start_time))
            
            
        game = Game(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1.user_name,p2.user_name,str({'x':0,'y':4}),str({'x':4,'y':0}),1)





def step(board,player,player_1_pos,player_2_pos,eps,is_finished):
    new_board = board
    new_position = player_1_pos if player == 1 else player_2_pos
    player_pos = new_position
    move_not_valid = set([])
    move = ""
    while new_position == player_pos and not is_finished:
        try:

            if len(move_not_valid) >= 1:
                move = take_action(board,player_1_pos,player_2_pos,player,1.0)
            else:
                move = take_action(board,player_1_pos,player_2_pos,player,eps)
            new_position,new_board,captured_position,is_finished,winner  = handle_move(actions[move],player_1_pos if player == 1 else player_2_pos,board,player)
            
            q_table_old = get_q_table(board, player_1_pos, player_2_pos, current_player)
            
            if player == 1 : player_1_pos = new_position
            else : player_2_pos = new_position

            q_table_new = get_q_table(board, player_1_pos, player_2_pos, current_player)
            reward_max = q_table_new.get_max_expected_reward()
            reward = len(captured_position)

            if winner != 0:
                if winner == player: reward += 10
                else : reward -= 10
                
            q_table_old.update(move,reward,reward_max)

        except Exception as err:
            move_not_valid.add(move)
            player_pos = player_1_pos if player == 1 else player_2_pos

    return new_position,new_board,is_finished

def take_action(board,player_1_pos,player_2_pos,current_player,eps):
    if random.uniform(0, 1) < eps:
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
#         new_player_pos,new_board,captured_positions,is_finished,winner = handle_move(actions[action],old_player_pos,old_board,current_player)
#     if is_finished:
#         raise Exception("Game finished")
#     return new_board, new_player_pos



# def calculate_reward(old_board,new_board, player):
#     """
#     Calculate the reward for the current state
#     """
#     return 0
    


