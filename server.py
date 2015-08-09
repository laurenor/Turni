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
# **** CHALLONGE API CALLS **** -- not using right now, because I will be at first
# storing info from a completed tournament.

CHALLONGE_API_KEY = os.environ.get('CHALLONGE_API_KEY')
challonge.set_credentials('lencat', 'CHALLONGE_API_KEY')

##############################################################################


r1 = requests.get('https://api.challonge.com/v1/tournaments/turni_test1.json', auth=('lencat', CHALLONGE_API_KEY))
tournament_data = r1.json()

r2 = requests.get('https://api.challonge.com/v1/tournaments/turni_test1/participants.json', auth=('lencat', CHALLONGE_API_KEY))
participant_data = r2.json()

r3 = requests.get('https://api.challonge.com/v1/tournaments/turni_test1/matches.json', auth=('lencat', CHALLONGE_API_KEY))
match_data = r3.json()


# counts number of matches to determine how many stations there will be
# total_stations = 0
# for i in range(len(match_data)-1):
# 	if match_data[i]['match']['round'] == 1:
# 		total_stations += 1
# print '** AMT OF STATIONS **: ', total_stations

# players = {}
# for i in range(len(participant_data)-1):
# 	player_id = participant_data[i]['participant']['id']
# 	player_name = participant_data[i]['participant']['username']
# 	players[player_id] = player_name

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
# used in /map
match_list = []
for i in range(len(match_data)-1):
	if match_data[i]['match']['state'] == "open":
		match_list.append(' vs. '.join(map(str,(match_data[i]['match']['player1_id'], match_data[i]['match']['player2_id']))))
print "*** MATCHES ***: ", pprint.pprint(match_list)




@app.route('/')
def index():
	"""Return index page"""

	print '**session**', session
	print tournament_data['tournament']['id']

	return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')
	user_type = request.form.get('user_type')

	user = User.query.filter_by(username=username).first()


	if user:
		session['loggedin'] = user.username
		flash('Successfully Logged In')
		return redirect('/profile/%s' % user.username)

	else:
		user = User(username=username, email=email, password=password, user_type=user_type)
		db.session.add(user)
		db.session.commit()
		session['loggedin'] = user.username 
		return redirect('/profile/%s' % user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')
	user_type = request.form.get('user_type')
	confirm = request.form.get('confirm')

	user = User.query.filter_by(username=username, password=password).first()

	if user:
		session['loggedin'] = user.username
		print '**session**', session
		flash('Successfully Logged In')
		return redirect('/profile/%s' % username)
	else:
		flash('Username / Password combination not found.  Please register first.')
		return redirect(url_for('register_user'))


@app.route('/logout')
def logout_user():
    """Log out the user"""
    session.clear()
    print '**session**', session
    return redirect('/')

@app.route('/about')
def about():
	"""Return about page"""
	return render_template('about.html')

@app.route('/create-map')
def create_map():
	"""Shows map creation form"""
	return render_template('create-map.html')

@app.route('/user-register')
def register_user():
	"""Shows registration page"""
	return render_template('register.html')

@app.route('/user-login')
def login_user():
	"""Shows registration page"""
	return render_template('login.html')

@app.route('/profile/<string:username>')
def user_profile(username):
	"""Show user's details and list of maps or tournaments participated in"""

	if session:
		user = User.query.filter_by(username=username).first()
		print "******user.username", user.username
		return render_template('user-profile.html', user=user.username)
	else:
		return render_template('login.html', user=user.username)


@app.route('/features')
def features():
	return render_template('features.html')

@app.route('/map')
def map():
	challonge_name = request.args.get('challonge_name')
	challonge_email = request.args.get('challonge_email')
	url = request.args.get('url')
	stream = request.args.get('stream')
	tourn_name = request.args.get('tourn_name')

	# adds all participants in tournament to the page
	all_players = []
	for i in range(len(participant_data)-1):
		player_id = participant_data[i]['participant']['username']
		all_players.append(player_id)

	# counts number of matches to determine how many stations there will be
	total_stations = 0
	for i in range(len(match_data)-1):
		if match_data[i]['match']['round'] == 1:
			total_stations += 1

	for i in range(len(participant_data)-1):
		player = Player.query.filter_by()
		challonge_name = str(participant_data[i]['participant']['username'])
		print "**Challonge name: ", challonge_name
		challonge_id = int(participant_data[i]['participant']['id'])
		print "**Challonge id: ", challonge_id
		player = Player.query.filter_by(challonge_name=challonge_name, challonge_id=challonge_id)
		if not player:
			new_player = Player(challonge_name=challonge_name, challonge_id=challonge_id)
			db.session.add(new_player)
	db.session.commit()


	# if url == tournament_data['tournament']['url']: 
	return render_template('map.html', 
							all_players=all_players, 
							tourn_name=tourn_name,
							challonge_name=challonge_name, 
							challonge_email=challonge_email, 
							url=url, 
							stream=stream, 
							match_list=match_list)
	# else:
	# 	return render_template('map.html', challonge_name=challonge_name, challonge_email=challonge_email, url=url, stream=stream, match_list=match_list)	



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()