import requests
import os
from flask import Flask, flash, render_template, redirect, json, request, session, url_for, send_from_directory
from jinja2 import StrictUndefined
import challonge
from model import User, Player, Station, StationPlayer, Tournament, connect_to_db, db
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

# counts number of matches to determine how many stations there will be
# total_stations = 0
# for i in range(len(match_data)-1):
# 	if match_data[i]['match']['round'] == 1:
# 		total_stations += 1
# print '** AMT OF STATIONS **: ', total_stations

# players = {}
# for i in range(len(participant_data)-1):
# 	challonge_id = participant_data[i]['participant']['id']
# 	player_name = participant_data[i]['participant']['username']
# 	players[challonge_id] = player_name

# print "*** DICT OF PLAYERS **: ", pprint.pprint(players)

######## FIXME: works with alphacpu
# using lists
# player1_list = []
# player2_list = []
# for i in range(len(match_data)-1): 
# 	# if match_data[i]['match']['round'] == 1:
# 	for j in range(len(participant_data)-1):
# 		if participant_data[j]['participant']['id'] == match_data[i]['match']['player1_id']:
# 			player1_list.append(str(participant_data[j]['participant']['username']))
# 		elif participant_data[j]['participant']['id'] == match_data[i]['match']['player2_id']:
# 			player2_list.append(str(participant_data[j]['participant']['username']))

# print "*** PLAYER 1 LIST ***: ", pprint.pprint(player1_list)
# print "*** PLAYER 2 LIST ***: ", pprint.pprint(player2_list)

# match_list = []
# for i in range(len(player1_list)-1):
# 	match_list.append(' vs. '.join(map(str,(player1_list[i], player2_list[i]))))
# print "*** MATCHES ***: ", pprint.pprint(match_list)


######## FIXME: doesn't list names; just IDs



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
	"""Signs user in if username and pw match; flashes '...invalid' if not"""
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

		url = request.args.get('url')
		stream = request.args.get('stream')
		tournament_name = request.args.get('tournament_name')

		r1 = requests.get('https://api.challonge.com/v1/tournaments/' + url + '.json', auth=('lencat', CHALLONGE_API_KEY))
		tournament_data = r1.json()

		r2 = requests.get('https://api.challonge.com/v1/tournaments/' + url + '/participants.json', auth=('lencat', CHALLONGE_API_KEY))
		participant_data = r2.json()

		r3 = requests.get('https://api.challonge.com/v1/tournaments/' + url + '/matches.json', auth=('lencat', CHALLONGE_API_KEY))
		match_data = r3.json()

		# creates list of matches ('Player1 vs. Player2')
		match_list = set_match_info(match_data)

		# list of all players
		all_players = get_all_players(participant_data)
			
		# adds player(s) to database, if player(s) not already in DB
		Player.add_to_db(participant_data)

		# FIXME: calculates max # of stations; should be helper function 
		max_stations = set_max_stations(match_data)


		# adds new tournament info if tournament is not yet in database
		tournament = Tournament.query.filter(tournament_name==tournament_name).first()
		if not tournament:
			user = User.query.filter_by(username=session['username']).first()
			print user
			tournament = Tournament(tournament_name=tournament_name, max_stations=max_stations, user_id=user.user_id)
			db.session.add(tournament)
		db.session.commit()

		open_stations = create_open_stations(tournament)
		print open_stations

		# adds station_id and tournament_id info to database
		Station.add_to_db(max_stations, tournament)

		# adds info on which stations players are at to database
		StationPlayer.add_to_db(match_data, open_stations)

		update_open_stations(open_stations)

		return render_template('map.html', 
								all_players=all_players, 
								tournament_name=tournament_name, 
								url=url, 
								stream=stream, 
								match_list=match_list,
								max_stations=max_stations,
								username=username)

@app.route('/save-map', methods=['POST'])
def save_map():
	"""Add body content of map to database"""

	body = request.form.get('body')

	user = User.query.filter_by(username=session['username']).first()
	tournament = Tournament.query.filter_by(user_id=user.user_id).first()
	savedmap = SavedMap(html=body, user_id=user.user_id, tournament_id=tournament.tournament_id)

	db.session.add(map_save_state)
	db.session.commit()

	return 'Your map has been saved.'

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
		if match_data[i]['match']['state'] == "open":
			match_list.append(' vs. '.join((str(match_data[i]['match']['player1_id']), (str(match_data[i]['match']['player2_id'])))))
	return match_list

def set_max_stations(match_data):
	"""Provides # of stations in venue"""
	max_stations = 0
	for i in range(len(match_data)-1):
		if match_data[i]['match']['state'] == 'open':
			max_stations += 1
	return max_stations

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