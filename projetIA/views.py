from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_sock import Sock
app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sock = Sock(app)
import werkzeug

from .business import *
from .ai import train_ai,take_action
from .models import db,Game,Player,init_db
actions = ['up','down','left','right']


@app.route('/', methods=['GET','POST'])
def index():
	
	if request.method == 'POST':
		session['pseudo'] = request.form['pseudo']
		if not session.get('pseudo'):
			flash('Pseudo is required!')
		else:
			p2 = Player.query.get('AI2')
			p1 = Player.query.get(session['pseudo'])
			if p1 is None:
				p1 = Player(session['pseudo'],False)
				db.session.add(p1)
				db.session.commit()

			game = Game(parser_string([[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,0]]),p1.user_name,p2.user_name,str({'x':0,'y':4}),str({'x':4,'y':0}),2)
			db.session.add(game)
			db.session.commit()
			session['GameId'] = game.id
			return redirect(url_for('game'))
	return render_template('index.html')

@app.route('/game',methods=['GET'])
def game():
	return render_template('game.html',player=session['pseudo'])

@app.route('/move', methods=['POST','GET'])
def move():
	if request.method == 'POST':
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
		move_not_valid = set([])
		while not is_valid:
			try : 
				game = Game.query.get(session['GameId'])
				if len(move_not_valid) >= 1:
					move = take_action(game.board,game.get_position('player1pos'),game.get_position('player2pos'),1,0.0)
				else:
					move = take_action(game.board,game.get_position('player1pos'),game.get_position('player2pos'),1,1.0)
				print(actions[move])
				result = do_move(actions[move], 'player1pos', 1);
				is_valid = True	
			except Exception as err:
				print(err)
				move_not_valid.add(move)
				continue
		return result

def do_move(move,player_pos,player):
	try :
		
		game = Game.query.get(session['GameId'])
		
		new_position, board, captured_positions, is_finished, winner = handle_move(move,game.get_position(player_pos),game.board,player);
		game.board = board
		game.set_position(player_pos,new_position)
		db.session.commit()
		return {"newPosition":new_position,"isFinished":is_finished, "board":board,"capturedPositions":captured_positions,"winner":winner}
	except Exception as err:
		raise Exception(err)
	
@sock.route('/trainSocket', methods=['GET'])
def train(ws):
	while True :
		data = ws.receive()
		data = int(data)
		if data in [10,100,1000,10000]:
			train_ai(ws, data)
			ws.send('done')



@app.route('/train', methods=['GET'])
def render_train():
	return render_template('train.html')

@app.route('/init', methods=['GET'])
def init():
	init_db()
	return 'done'

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_500(error):
	return 'Bad move', 500




