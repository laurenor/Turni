import requests
import os
from flask import Flask, render_template, redirect, json
from jinja2 import StrictUndefined
import model
import challonge

app = Flask(__name__)
app.secret_key = 'ABC'
app.jinja_env.undefined = StrictUndefined


##############################################################################
# # Challonge API

# app.CHALLONGE_API_KEY = os.environ.get('CHALLONGE_API_KEY')
# challonge.set_credentials('lencat', 'CHALLONGE_API_KEY')

# tournament = challonge.tournaments.show(1829931)
# # ^for tournament info to populate for users, the tournament ID should be taken from a form

# # # get participant info
# # req = requests.get('https://api.challonge.com/v1/tournaments/turni_test1/participants.json', auth=('lencat', 'CHALLONGE_API_KEY'))
# # participant_info = req.json()

# # #get match info
# # req1 = requests.get('https://api.challonge.com/v1/tournaments/turni_test1/matches.json', auth=('lencat', 'CHALLONGE_API_KEY'))
# # match_info = req1.json()

# # Tournaments, matches, and participants are all represented as normal Python dicts.
# print(tournament["id"]) # 3272
# print(tournament["name"]) # My Awesome Tournament
# print(tournament["started-at"]) # None

# # Retrieve the participants for a given tournament.
# participants = challonge.participants.index(tournament["id"])
# print(len(participants)) # 13

##############################################################################




@app.route('/')
def index():
	"""Return index page"""
	
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')
	confirm = request.form.get('confirm')

@app.route('/about')
def about():
	"""Return about page"""

	return render_template('about.html')

@app.route('/create-map')
def create_map():
	return render_template('create-map.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/participant-list')
def all_participants():
	participants = []
	for i in range(len(doc)-1):
		participants.append(participant_info[i]['participant']['challonge_username'])
	return str(participants)

# user login 
# login_manager = LoginManager()



if __name__ == "__main__":
    app.run(debug=True)