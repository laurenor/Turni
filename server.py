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
from twilio import twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)

app.secret_key = 'ABC'
app.jinja_env.undefined = StrictUndefined


##############################################################################
# **** CHALLONGE **** 

CHALLONGE_API_KEY = os.environ.get('CHALLONGE_API_KEY')
challonge.set_credentials('lencat', 'CHALLONGE_API_KEY')

##############################################################################
# **** Twilio **** 

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(account_sid, auth_token)
to_number= os.environ['TWILIO_TO_NUMBER']
TWILIO_NUMBER = os.environ['TWILIO_NUMBER']

##############################################################################

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

		tournaments = db.session.query(Tournament.tournament_name).join(User).filter(user.user_id==Tournament.user_id).all()

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

@app.route('/map', methods=['GET', 'POST'])
def map():
	if 'username' in session:
		username = session['username']


	if request.method == 'POST':

		url = request.form.get('url')
		stream = request.form.get('stream')
		tournament_name = request.form.get('tournament_name')
		open_stations = request.form.get('open_stations')

		# API calls #######################################################################################

		r2 = requests.get('https://api.challonge.com/v1/tournaments/'+url+'/participants.json', auth=('lencat', CHALLONGE_API_KEY))
		participant_data = r2.json()

		r3 = requests.get('https://api.challonge.com/v1/tournaments/'+url+'/matches.json', auth=('lencat', CHALLONGE_API_KEY))
		match_data = r3.json()

		players = {}
		for i in range(len(participant_data)):
			challonge_id = str(participant_data[i]['participant']['id'])
			player_name = participant_data[i]['participant']['name']
			players[challonge_id] = player_name

		all_matches = []

		rounds = []
		for i in range(len(match_data)-1):
			if match_data[i]['match']['round'] not in rounds:
				rounds.append(match_data[i]['match']['round'])

		round_count = {}
		for num in rounds:
			for i in range(len(match_data)):
				if (match_data[i]['match']['round'] == num) and (match_data[i]['match']['round'] not in round_count):
					round_count[num] = 1
				elif (match_data[i]['match']['round'] == num) and (match_data[i]['match']['round'] in round_count):
					round_count[num] += 1

			highest = round_count[rounds[0]]
			most_round = rounds[0]
			if round_count[num] > highest :
				highest = round_count[num]
				most_round = num

		max_stations = highest

		####################################################################################################


		all_players = get_all_players(participant_data)

		user = User.query.filter_by(username=session['username']).first()
		tournament = Tournament.query.filter_by(tournament_name=tournament_name).first() 


		if not tournament:
			tournament = Tournament(tournament_name=tournament_name, max_stations=max_stations, user_id=user.user_id, url=url, stream=stream)
			db.session.add(tournament)
		db.session.commit()

		tables = tournament.max_stations
		length_all_players = len(all_players)

		return render_template('map.html', 
						tables=json.dumps(tables), 
						all_matches=json.dumps(all_matches), 
						username=username,
						all_players=all_players,
						max_stations=max_stations,
						url=url,
						stream=stream,
						tournament_name=tournament_name,
						players=json.dumps(players),
						length_all_players=length_all_players,
						open_stations=open_stations
						)

	elif request.method == 'GET':

		tournament_name = request.args.get('tournament_name')
		print "***tournament: ", tournament_name
		tournament = Tournament.query.filter_by(tournament_name=tournament_name).first()
		print "***tournament: ", tournament
		tables = tournament.max_stations
		user = User.query.filter_by(username=session['username']).first()
		url = tournament.url
		stream = tournament.stream
		max_stations = tournament.max_stations
		open_stations = 5

		r2 = requests.get('https://api.challonge.com/v1/tournaments/'+url+'/participants.json', auth=('lencat', CHALLONGE_API_KEY))
		participant_data = r2.json()

		r3 = requests.get('https://api.challonge.com/v1/tournaments/'+url+'/matches.json', auth=('lencat', CHALLONGE_API_KEY))
		match_data = r3.json()

		players = {}
		for i in range(len(participant_data)):
			challonge_id = str(participant_data[i]['participant']['id'])
			player_name = participant_data[i]['participant']['name']
			players[challonge_id] = player_name

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
					match_list.append(mylist)
			all_matches.append(match_list)

		all_players = get_all_players(participant_data)
		length_all_players = len(all_players)


		return render_template('map.html', 
								tables=json.dumps(tables), 
								all_matches=json.dumps(all_matches), 
								username=username,
								all_players=all_players,
								max_stations=max_stations,
								url=url,
								stream=stream,
								tournament_name=tournament_name,
								players=json.dumps(players),
								length_all_players=length_all_players,
								open_stations=open_stations
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
	tournament_name = request.form.get('tournament_name')

	user = User.query.filter_by(username=session['username']).first()

	tournament = Tournament.query.filter_by(tournament_name=tournament_name).first()
	position = Position.query.filter(Position.table_id==table_id, Position.tournament_id==tournament.tournament_id).first()
	print "***tournament: ", tournament.tournament_id

	if not position:
		print "***not position: "
		coordinates = Position(table_id=table_id, left=left, top=top, tournament_id=tournament.tournament_id)
		db.session.add(coordinates)
	else:
		print "***else position"
		position.table_id=table_id
		position.left=left
		position.top=top
		
	db.session.commit()

	return "Your changes have been saved!"

@app.route('/get-coords')
def get_coords():
	tournament_name = request.args.get('tournament_name')
	print "***get_coords tourn name: ", tournament_name

	tournament = Tournament.query.filter_by(tournament_name=tournament_name).first()
	tournament_id = tournament.tournament_id

	positions = db.session.query(Position.table_id, Position.left, Position.top).filter(Position.tournament_id==tournament_id).all();
	posijson = json.dumps(positions)
	print "****posijson: ", posijson
	return posijson

@app.route('/delete-tourn', methods=['POST'])
def delete_tourn():
	tournament_name = request.form.get('tournament_name')
	print "***Tournament_name: ", tournament_name

	tournament = Tournament.query.filter_by(tournament_name=tournament_name).first()
	print "***Tournament: ", tournament
	
	matches = Match.query.filter(Match.tournament_id == tournament.tournament_id).all()
	positions = Position.query.filter(Position.tournament_id == tournament.tournament_id).all()
	tournaments = Tournament.query.filter(Tournament.tournament_id == tournament.tournament_id).all()

	for position in positions:
		db.session.delete(position)	
	db.session.commit()

	for tournament in tournaments:
		db.session.delete(tournament)
	db.session.commit()


	print "***Tournament_id: ", tournament.tournament_id

	return "Tournament has been deleted."

@app.route('/contact')
def contact():

	if 'username' in session:
		username = session['username']
	
		return render_template('contact.html', username=username)

	else: 
		return render_template('contact.html')

@app.route('/mock-json')
def mock():

	json_data = open(os.path.join('./json/', "turni.json"), "r")
	read_file = json_data.read()
	json_file = json.loads(read_file)


	matches = sorted(json_file, key=lambda k: k['match']['updated_at'])


	matches_list = []
	for match in matches:
		matches_list.append(match['match'])

	matches_json = json.dumps(matches_list)

	return matches_json

######################################################## twilio

@app.route('/twilio', methods=['POST'])
def twilio():
	text_message = request.form.get('text_message')
	message=client.messages.create(from_=TWILIO_NUMBER, to=to_number, body=text_message)

	print message.sid

	return text_message 

###########################################
# helper functions

def get_all_players(participant_data):
	"""Creates list of all players in tournament"""
	all_players = []
	for i in range(len(participant_data)):
		challonge_id = participant_data[i]['participant']['username']
		if challonge_id is not None:
			all_players.append(challonge_id)
		else:
			challonge_id = participant_data[i]['participant']['name']
			all_players.append(challonge_id)

	dict_all_players = {}

	count = 0
	for player in all_players:
			dict_all_players[player] = count
			count += 1
	return dict_all_players

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