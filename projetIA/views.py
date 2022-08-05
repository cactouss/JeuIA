from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session, jsonify
app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config.from_object('config')

import werkzeug

from .business import *
from .train import train_ai
from .models import init_db,db


from uuid import uuid4




min = 0
max = 4
data_games = {}
scores = [
	{'pseudo':'Isa','points':'100'},
	{'pseudo':'ISA','points':'200'}
]

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		session['pseudo'] = request.form['pseudo']
		if not session.get('pseudo'):
			flash('Pseudo is required!')
		else:
			session['board'] = parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]])
			session['player1pos'] = {'x':0,'y':4}
			session['player2pos'] = {'x':4,'y':0}
			session['uuid'] = uuid4()
			return redirect(url_for('game'))
	return render_template('index.html', scores=scores)

@app.route('/game',methods=['GET'])
def game():
	return render_template('game.html',player=session['pseudo'])

@app.route('/move', methods=['POST','GET'])
def move():
	if request.method == 'POST':
		#print all the data of request.form
		move = request.get_json()['move']
		if not move:
			raise Exception("Move is required")
		else:
			try:
				return do_move(move, 'player2pos', 2);
			except Exception as e:
				return handle_500(e)
			
				

	if request.method == 'GET':
		is_valid = False
		while not is_valid:
			try : 
				move = random_move()
				result = do_move(move, 'player1pos', 1);
				is_valid = True
				print(move," is ok")	
			except Exception as err:
				print("")
		return result

def do_move(move,player_pos,player):
	try :
		new_position, board, captured_positions, is_finished, winner = handle_move(move,session[player_pos],session['board'],player);
		print(f"new position : {new_position} , board : {board} , captured_positions : {captured_positions} , is_finished : {is_finished}")
		session['board'] = board
		session[player_pos] = new_position	
		return {"newPosition":new_position,"isFinished":is_finished, "board":board,"capturedPositions":captured_positions}
	except Exception as err:
		raise Exception(err)
	
@app.route('/result', methods=['GET'])
def result():
	return render_template('result.html',player=session['pseudo'],board = session['board'])

@app.route('/train', methods=['GET'])
def train():
	init_db()
	train_ai()
	return handle_500("Training en cours")

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_500(error):
	return 'Bad Move', 500




