import re
from unittest.loader import VALID_MODULE_NAME
from flask import Flask, render_template, request, url_for, flash, redirect,request
from sqlalchemy import table
from random import randint
from flask_socketio import SocketIO, emit
from .business import *

app = Flask(__name__)

socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config.from_object('config')


games = {} #var Global

@socketio.on('connect')
def handle_connect() :
	#crée une fonction dans business pour géré la connection -> arg request pour trouver le sid 
	games[request.sid] = randint(1,1000)#set une clé dans le dico avec la valeur personnel clé = session id 
	emit('message',{"data":request.sid})

@socketio.on('Move')
def handle_move(move):
	#move array[x,y]
	# -1=>x y <= 1 && x et y pas 0 en même temps
	emit('message',games[request.sid])

@socketio.on('disconnect')
def deco():
	games.pop(request.sid)#quand l'utilisateur se déco supprime la clé



scores = [
	{'pseudo':'Isa','points':'100'},
	{'pseudo':'ISA','points':'200'}
]

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
