import random
from .views import app
from flask_sqlalchemy import SQLAlchemy
import logging as lg
import ast

db = SQLAlchemy(app,session_options={"autoflush": False})
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    lg.warning('Database initialized!')
    # definition des modèles
    #region 11/11
    p1 = Player("AI1",True)
    p2 = Player("AI2",True)

    #endregion
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()


	# définition des modèles
class Player(db.Model):
    user_name = db.Column(db.String(200), primary_key=True)
    is_ai = db.Column(db.Boolean, nullable=False)

    def __init__(self,user_name,is_ai):
        self.user_name = user_name
        self.is_ai = is_ai


    def getId(self):
        return self.user_name

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board = db.Column(db.String(200), nullable=False)
    player_1 = db.Column(db.String(200), db.ForeignKey('player.user_name'))
    player_2 = db.Column(db.String(200), db.ForeignKey('player.user_name'))
    player_1_pos = db.Column(db.String(200), nullable=False)
    player_2_pos = db.Column(db.String(200), nullable=False)
    current_player = db.Column(db.Integer, nullable=False)

    def __init__(self,board,player_1,player_2,player_1_pos,player_2_pos,current_player):
        self.board = str(board)
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_pos = str(player_1_pos)
        self.player_2_pos = str(player_2_pos)
        self.current_player = current_player
    def get_position(self,position):
        if position == "player2pos":
            return ast.literal_eval(self.player_2_pos)
        else:
            return ast.literal_eval(self.player_1_pos)
    def set_position(self,player,position):
        if player == "player2pos":
            self.player_2_pos = str(position)
        else:
            self.player_1_pos = str(position)

class Q_table(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    q_up = db.Column(db.Float, nullable=False,default=0)
    q_down = db.Column(db.Float, nullable=False,default=0)
    q_left = db.Column(db.Float, nullable=False,default=0)
    q_right = db.Column(db.Float, nullable=False,default=0)

    def __init__(self,position):
        self.id = position
        self.q_up = 0
        self.q_down = 0
        self.q_left = 0
        self.q_right = 0

    def getId(self):
        return self.id
        
    def Q_values (self):
        return [self.q_up, self.q_down, self.q_left, self.q_right]
    
    def get_best_action(self):
        q_values = self.Q_values()
        max_value = max(q_values)
        if max_value == 0:
            return random.randint(0,3)
        else:
            return q_values.index(max_value)

    def get_max_expected_reward(self):
        return max(self.Q_values())



