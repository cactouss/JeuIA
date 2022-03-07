from flask_sqlalchemy import SQLAlchemy
from .views import app
import logging as lg

db = SQLAlchemy(app)

def init_db():
	db.drop_all()
	db.create_all()

	db.session.commit()
	lg.warning('Database initialized !')

	# définition des modèles


game_bord = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
min = 0
max = 4
def is_valid_move(position,move,player):
	if move == "up" and position.y > min:
		position.y -= 1	
	elif move == "down" and position.y < max:
		position.y += 1
	elif move == "left" and position.x > min:
		position.x -= 1
	elif move == "right" and position.x < max:
		position.x -= 1
	else: return false

	if game_bord[position.x][position.y] == 0:
		game_bord[position.x][position.y] = player
		return true
	else:
		return false

def enclos(player):
	restart = true
	while restart:
		restart = false
		for col in range(5):
			for line in range(5):
				if game_bord[col][line] == 0:
					if line > min:
						up = 1 if game_bord[col][line-1] == player else 0
					else:
						up = 0
					if line < max:
						down = 1 if game_bord[col][line+1] == player else 0
					else:
						down = 0
					if col > min:
						left = 1 if game_bord[col-1][line] == player else 0
					else:
						left = 0
					if col < max:
						right = 1 if game_bord[col+1][line] == player else 0
					else:
						right = 0
					
					if up + down + left + right >= 3:
						game_bord[col][line] = player
						restart = true
						break
