import requests
import os
from flask import Flask, flash, render_template, redirect, json, request, session, url_for, jsonify
from jinja2 import StrictUndefined
import challonge
from model import User, Tournament, Match, Position, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager, UserMixin, login_required
import hashlib # for email hashing
import pprint

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'ABC'
app.jinja_env.undefined = StrictUndefined


##############################################################################
# **** CHALLONGE API CALLS **** 

CHALLONGE_API_KEY = os.environ.get('CHALLONGE_API_KEY')
challonge.set_credentials('lencat', 'CHALLONGE_API_KEY')

##############################################################################


r3 = requests.get('https://api.challonge.com/v1/tournaments/alphacpu/matches.json', auth=('lencat', CHALLONGE_API_KEY))
match_data = r3.json()

r2 = requests.get('https://api.challonge.com/v1/tournaments/alphacpu/participants.json', auth=('lencat', CHALLONGE_API_KEY))
participant_data = r2.json()

r3 = requests.get('https://api.challonge.com/v1/tournaments/alphacpu/matches.json', auth=('lencat', CHALLONGE_API_KEY))
match_data = r3.json()

players = {}
for i in range(len(participant_data)):
	challonge_id = participant_data[i]['participant']['id']
	player_name = participant_data[i]['participant']['name']
	players[challonge_id] = player_name

# print "*** DICT OF PLAYERS **: ", pprint.pprint(players)

all_matches = []


for j in range(6):
	match_list = []
	for i in range(len(match_data)):
		if match_data[i]['match']['round'] == j+1:
			mylist = [ match_data[i]['match']['player1_id'], match_data[i]['match']['player2_id'] ]
			for i in range(len(mylist)):
				for key in players:
					if mylist[i] == key:
						mylist[i] = players[key]
			match_list.append(' vs. '.join(map(str, mylist)))
	all_matches.append(match_list)
	print "Round ", j+1, ": ", match_list

print "***all_matches: ", all_matches




rounds = []
for i in range(len(match_data)-1):
	if match_data[i]['match']['round'] not in rounds:
		rounds.append(match_data[i]['match']['round'])
print "ROUNDS: ", rounds

round_count = {}
for num in rounds:
	for i in range(len(match_data)):
		if (match_data[i]['match']['round'] == num) and (match_data[i]['match']['round'] not in round_count):
			round_count[num] = 1
		elif (match_data[i]['match']['round'] == num) and (match_data[i]['match']['round'] in round_count):
			round_count[num] += 1
	print "**round count: ", round_count 
	highest = round_count[rounds[0]]
	most_round = rounds[0]
	if round_count[num] > highest :
		highest = round_count[num]
		most_round = num
print "**Round with most matches: ", most_round

# used in /map
max_stations = highest



@app.route('/')
def index():
	"""Return index page"""

	if 'username' in session:
		username = session['username']
		return render_template('index.html', username=username)
	else:
		return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Registers user if username not already in DB; if user in database, flash error."""
	if request.method == 'POST':
		username = request.form.get('username')
		email = request.form.get('email')
		password = request.form.get('password')
		user_type = request.form.get('user_type')
		phone = request.form.get('phone')

		user = User.query.filter_by(username=username).first()

		if user:
			# session['username'] = user.username
			flash('That username already exists!')
			return render_template('register.html')

		else:
			user = User(username=username, email=email, password=password, user_type=user_type, phone=phone)
			db.session.add(user)
			db.session.commit()
			session['username'] = user.username 
			return redirect('/profile/%s' % user.username)
	else:
		return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Signs user in if username and pw match; flashes '...invalid' if not"""
	if request.method == 'POST':	
		username = request.form.get('username')
		email = request.form.get('email')
		password = request.form.get('password')
		user_type = request.form.get('user_type')
		confirm = request.form.get('confirm')

		user = User.query.filter_by(username=username, password=password).first()

		if user:
			session['username'] = user.username
			flash('Successfully Logged In')
			return redirect('/profile/%s' % user.username)
		else:
			flash('Username and/or password is invalid.')
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/logout')
def logout_user():
    """Log out the user"""
    session.clear()
    flash('Successfully logged out.')
    return redirect('/')

@app.route('/about')
def about():
	"""Return about page"""
	if 'username' in session:
		username = session['username']
		return render_template('about.html', username=username)
	else:
		return render_template('about.html')

@app.route('/create-map')
def create_map():
	"""Shows map creation form"""
	if 'username' in session:
		username = session['username']
		return render_template('create-map.html', username=username)
	else:
		return render_template('create-map.html', username=username)

@app.route('/profile/<string:username>')
def user_profile(username):
	"""Show user's details and list of maps or tournaments participated in"""

	if session:
		user = User.query.filter_by(username=username).first()
		print "******user.username", user.username

		tournaments = db.session.query(Tournament.tournament_name).join(User).filter(user.user_id==Tournament.user_id).all()
		print "***list of tournaments: ", tournaments

		# removes unicode formatting on tournament names 
		str_tournaments = []
		for tourn in tournaments:
			str_tournaments.append(tourn[0])


		amt_of_tourns = []

		for i in range(len(tournaments)):
			amt_of_tourns.append(i+1)
		print amt_of_tourns

		return render_template('user-profile.html', username=user.username, tournaments=str_tournaments, amt_of_tourns=amt_of_tourns)
	else:
		return render_template('login.html', user=user.username)


@app.route('/features')
def features():
	"""Shows features page"""
	if 'username' in session:
		username = session['username']
		return render_template('features.html', username=username)
	else:
		return render_template('features.html')

@app.route('/map', methods=['GET','POST'])
def map():
	if 'username' in session:
		username = session['username']

	if request.method == 'POST':
		url = 'alphacpu'
		stream = request.form.get('stream')
		tournament_name = request.form.get('tournament_name')

		# puts all player names on page
		all_players = get_all_players(participant_data)

		# adds new tournament info if tournament is not yet in database
		user = User.query.filter_by(username=session['username']).first()
		tournament = Tournament.query.filter(tournament_name==tournament_name).first()
		print "***user!! :", user
		if not tournament:
			# user = User.query.filter_by(username=session['username']).first()
			tournament = Tournament(tournament_name=tournament_name, max_stations=max_stations, user_id=user.user_id)
			db.session.add(tournament)
		db.session.commit()

		open_stations = create_open_stations(tournament)

		for i in range(len(match_data)):
			match_id = match_data[i]['match']['id']
			round_num = match_data[i]['match']['round']
			player_1 = match_data[i]['match']['player1_id']
			player_2 = match_data[i]['match']['player2_id']
			tournament_id = tournament.tournament_id

			match = Match(tournament_id=tournament_id, match_id=match_id, round_num=round_num, player_1=player_1, player_2=player_2)
			db.session.add(match)
		db.session.commit()
		print len(match_data)

		return render_template('map.html', 
							all_players=all_players, 
							tournament_name=tournament_name, 
							stream=stream, 
							match_list=match_list,
							max_stations=max_stations,
							username=username,
							url=url,
							open_stations=open_stations)

		# else:
		# 	user = User.query.filter_by(username=session['username']).first()

		# 	all_players = 
		# 	tournament_name = 
		# 	url =
		# 	stream = 
		# 	match_list = 
		# 	max_stations =
		# 	username = 

		# 	return render_template('map.html', 
		# 							all_players=all_players, 
		# 							tournament_name=tournament_name, 
		# 							url=url, 
		# 							stream=stream, 
		# 							match_list=match_list,
		# 							max_stations=max_stations,
		# 							username=username)

@app.route('/map2')
def map2():

	tables = 16
	username = 'meowchi'
	all_players = get_all_players(participant_data)
	url = 'alphacpu'
	stream = 'http://twitch.tv'

	return render_template('maps2.html', 
							tables=json.dumps(tables), 
							all_matches=json.dumps(all_matches), 
							username=username,
							all_players=all_players,
							max_stations=max_stations,
							url=url,
							stream=stream,
							)

@app.route('/untitled')
def untitled():
	"""testing page"""
	username = "meowchi"



	return render_template('untitled.html', username=username)

@app.route('/add-coords', methods=['POST'])
def add_coords():

	from sqlalchemy import update

	left = request.form.get('left')
	top = request.form.get('top')
	table_id = request.form.get('table_id')

	position = Position.query.filter_by(table_id=table_id).first()

	if not position:
		coordinates = Position(table_id=table_id, left=left, top=top)
		db.session.add(coordinates)
	else:
		position.table_id=table_id
		position.left=left
		position.top=top
		
	db.session.commit()

	return "Your changes have been saved!"

@app.route('/get-coords')
def get_coords():
	positions = db.session.query(Position.table_id, Position.left, Position.top).all();
	posijson = json.dumps(positions)
	return posijson



###########################################
# helper functions
def get_all_players(participant_data):
	"""Creates list of all players in tournament"""
	all_players = []
	for i in range(len(participant_data)-1):
		challonge_id = participant_data[i]['participant']['username']
		if challonge_id is not None:
			all_players.append(challonge_id)
		else:
			challonge_id = participant_data[i]['participant']['name']
			all_players.append(challonge_id)
	return all_players

def set_match_info(match_data):
	"""Creates list of all matches in tournament"""
	match_list = []
	for i in range(len(match_data)-1):
		if match_data[i]['match']['round'] == "1":
			print "***what is MD: ", match_data[i]['match']['round']
			match_list.append(' vs. '.join((str(match_data[i]['match']['player1_id']), (str(match_data[i]['match']['player2_id'])))))
	return match_list


def set_max_stations(match_data):
	rounds = []
	for i in range(len(match_data)-1):
		if match_data[i]['match']['round'] not in rounds:
			rounds.append(match_data[i]['match']['round'])
	print "ROUNDS: ", rounds

	round_count = {}
	for num in rounds:
		for i in range(len(match_data)):
			if (match_data[i]['match']['round'] == num) and (match_data[i]['match']['round'] not in round_count):
				round_count[num] = 1
			elif (match_data[i]['match']['round'] == num) and (match_data[i]['match']['round'] in round_count):
				round_count[num] += 1
		print "**round count: ", round_count 
		highest = round_count[rounds[0]]
		most_round = rounds[0]
		if round_count[num] > highest :
			highest = round_count[num]
			most_round = num
	return highest

def create_open_stations(tournament):
	"""Creates a list of free (open) stations in tournament"""
	open_stations = []
	for i in range(tournament.max_stations):
		open_stations.append(i+1)
	print "***OPEN STATIONS 1: ", open_stations
	return open_stations

def update_open_stations(open_stations):

	tup_ids = db.session.query(StationPlayer.station_id).all()
	list_ids = [i[0] for i in tup_ids]
	# removing duplicates from list_ids
	set_ids = set(list_ids)
	list_ids = list(set_ids)

	for num in open_stations:
		if num in list_ids:
			open_stations.pop(num)
	print "***OPEN STATIONS 2: ", open_stations
	return open_stations
	

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()