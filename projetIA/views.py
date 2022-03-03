from flask import Flask, render_template, request, url_for, flash, redirect
app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config.from_object('config')

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
