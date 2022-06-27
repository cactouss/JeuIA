import imp
from typing import List
from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session, jsonify
from uuid import uuid4
from random import Random, randint
from .business import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config.from_object('config')

min = 0
max = 4
data_games = {}
scores = [
	{'pseudo':'Isa','points':'100'},
	{'pseudo':'ISA','points':'200'}
]




# @socketio.on('connect')
# def test_connect():
# 	data_games[request.sid] = {'board':[[1,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,2]],'player1pos':{'x':0,'y':0},'player2pos':{'x':4,'y':4}}

# 	# print('hey')
# 	# nombreDeBase = randint(1,1000)
# 	# test = {"data":nombreDeBase}
# 	# print(test)

# @socketio.on('move')
# def message(move):
# 	is_valid,new_position_1 = valid_move(data_games[request.sid]['player1pos'],move,data_games[request.sid]['board'],1)
# 	if(us_valid):
# 		new_position_2 = random_move(data_games[request.sid]['player2pos'],data_games[request.sid]['board'],2)
		
# 		past_position_1 = data_games[request.sid]['player1pos']
# 		past_position_2 = data_games[request.sid]['player2pos']

# 		data_games[request.sid]['player1pos'] = new_position_1
# 		data_games[request.sid]['player2pos'] = new_position_2

# 		board = data_games[request.sid]['board']
# 		board[new_position_1['x']][new_position_1['y']] = 1
# 		board[new_position_2['x']][new_position_2['y']] = 2
# 		data_games[request.sid]['board'] = board

# 		emit('moveChecked',(past_position_1,new_position_1,past_position_2,new_position_2))
# 		#print(test)
# 		#print(data['data'])
# 		#emit('move',test)

# current_player = {}

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
			flash('Move is required!')
			return {'status':500,'message':'Move is required!'}
		else:
			board = session['board']
			is_valid, new_board,caputred_position, new_position = handle_move(move,session['player2pos'],board,2)
			session['player2pos'] = new_position
			session['board'] = new_board
			is_finished = is_game_finished(new_board)
			if is_valid:
				session['player2pos'] = new_position
				if is_finished:
					return {'status':201}
				return {'status':200,'message':'Move is valid!','captured_position':caputred_position,'new_position':new_position}
			else:
				return {'status':500,'message':'Move is invalid!'}
	if request.method == 'GET':
		is_valid = False
		while not(is_valid) :
			board = session['board']
			move = random_move()
			print(move)
			is_valid, new_board,caputred_position, new_position = handle_move(move,session['player1pos'],board,1)
			session['player1pos'] = new_position
			session['board'] = new_board
		print(new_position)
		return {'status':200,'message':'Move is valid!','captured_position':caputred_position,'new_position':new_position}

			
@app.route('/result', methods=['GET'])
def result():
	return render_template('result.html',player=session['pseudo'],board = session['board'])