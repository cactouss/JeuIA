import random
from .business import *
from .models import *
import copy
eps = 0.9
NB_GAEMES_EXPLORATION = 1000
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

def train_ai(nb_games = 1000):
    """
    Train the AI
    """
    game = Game()
    state = game.board + game.player_1_pos + game.player2_pos + str(game.current_player)
    actions= ['up','down','left','right']
    game = Game(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1,p2,{'x':0,'y':4},{'x':4,'y':0},1)
    for i in range(nb_games):
        is_finished = False
        while not is_finished:
            p1 = Player.query.filter_by(user_name='AI1')
            p2 = Player.query.filter_by(user_name='AI2')
            
            db.session.add(game)
            nb_turn = 0
            eps = espylon_greedy(eps,game.id)
            while not is_finished:
                #player 1 move and update q tabkle
                try:
                    action = take_action(game.board,game.player_1_pos,game.player_2_pos,1,eps)
                    new_board, new_player_pos_P1 = take_step(game.board,game.player_1_pos,1,actions[action])
                except Exception as e:
                    #handle game finished
                    break
                try:
                    action_p2 = take_action(new_board,new_player_pos_P1,game.player_2_pos,2,0.0)
                    new_board_p2, new_player_pos_p2 = take_step(new_board,game.player_2_pos,2,actions[action_p2])
                except Exception as e:
                    #handle if game should be finished
                    print("")
                action_p1_1 = take_action(new_board_p2,new_player_pos_p2,new_player_pos_P1,1,0.00)
                #calculate reward and update q table
                game.board = new_board
                game.player1_pos = new_player_pos_P1
                game.current_player = 2

                #player 2 move and update q table
                try:
                    action = take_action(game.board,game.player_1_pos,game.player_2_pos,2,eps)
                    new_board, new_player_pos_P2 = take_step(game.board,game.player_2_pos,2,actions[action])
                except Exception as e:
                    #handle game finished
                    break
                try:
                    action_p1 = take_action(new_board,new_player_pos_P2,game.player_1_pos,1,0.0)
                    new_board_p1, new_player_pos_p1 = take_step(new_board,game.player_1_pos,1,actions[action_p2])
                except Exception as e:
                    #handle if game should be finished
                    print("")
                action_p1_1 = take_action(new_board_p1,new_player_pos_p2,new_player_pos_P1,2,0.0)
                game.board = new_board
                game.player2_pos = new_player_pos_P2
                game.current_player = 1
                nb_turn += 1
                #calculate reward and update q table 
        game.__init__(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1,p2,{'x':0,'y':4},{'x':4,'y':0},1) #reset game

                


                    

        eps = espylon_greedy(eps,game.id)

        print(f"training at game{(i+1/nb_games)*100} % ")
    


            
            
def take_step(board,current_player_pos,current_player,action):
    """
    Take a step in the game
    """
    old_player_pos = copy.copy(current_player_pos)
    old_board = copy.copy(board)
    new_player_pos = copy.copy(old_player_pos)
    while old_player_pos == new_player_pos:
        new_player_pos,new_board,captured_positions,is_finished = handle_move(actions[action],old_player_pos,old_board,current_player)
    if is_finished:
        raise Exception("Game finished")
    return new_board, new_player_pos



def calculate_reward(old_board,new_board, player):
    """
    Calculate the reward for the current state
    """
    return 0
    


