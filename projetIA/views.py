import imp
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_socketio import SocketIO, emit, send
from random import randint
from .test import valid_move,random_move

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config.from_object('config')
socketio = SocketIO(app)
min = 0
max = 4
data_games = {}
scores = [
	{'pseudo':'Isa','points':'100'},
	{'pseudo':'ISA','points':'200'}
]




@socketio.on('connect')
def test_connect():
	data_games[request.sid] = {'board':[[1,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,2]],'player1pos':{'x':0,'y':0},'player2pos':{'x':4,'y':4}}

	# print('hey')
	# nombreDeBase = randint(1,1000)
	# test = {"data":nombreDeBase}
	# print(test)

@socketio.on('move')
def message(move):
	is_valid,new_position_1 = valid_move(data_games[request.sid]['player1pos'],move,data_games[request.sid]['board'],1)
	if(us_valid):
		new_position_2 = random_move(data_games[request.sid]['player2pos'],data_games[request.sid]['board'],2)
		
		past_position_1 = data_games[request.sid]['player1pos']
		past_position_2 = data_games[request.sid]['player2pos']

		data_games[request.sid]['player1pos'] = new_position_1
		data_games[request.sid]['player2pos'] = new_position_2

		board = data_games[request.sid]['board']
		board[new_position_1['x']][new_position_1['y']] = 1
		board[new_position_2['x']][new_position_2['y']] = 2
		data_games[request.sid]['board'] = board

		emit('moveChecked',(past_position_1,new_position_1,past_position_2,new_position_2))
		#print(test)
		#print(data['data'])
		#emit('move',test)

current_player = {}

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		pseudo = request.form['pseudo']
		if not pseudo:
			flash('Pseudo is required!')
		else:
			global current_player 
			current_player = {'pseudo': pseudo, 'points': '0'}
			scores.append(current_player)
			return redirect(url_for('game'))
	return render_template('index.html', scores=scores)

@app.route('/game')
def game():
	return render_template('game.html',player=current_player)
