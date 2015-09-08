# Turni
<img src="/static/img/turni2.png" alt="Turni">
### What is Turni?
Turni is a web application for esports tournament organizers that creates interactive venue maps using data from <a href="http://api.challonge.com/v1" target="_blank">Challonge</a> and notifies participants via <a href="https://www.twilio.com/sms" target="_blank">Twilio SMS</a> of when and where they should go when it is their turn to play. With Turni, tournament organizers also have the option of having their Twitch stream, Twitch chat, and Challonge brackets embedded on their map page, so everything they need on tournament day will be available in a single browser window.

#### Technology Stack
JavaScript, jQuery, HTML5, CSS3, Bootstrap, Python, Flask, Jinja2, SQLAlchemy, PostgreSQL, jQuery UI Draggable and Resizable, AJAX

#### APIs
<a href="http://api.challonge.com/v1" target="_blank">Challonge</a>, <a href="https://www.twilio.com/sms" target="_blank">Twilio SMS</a>, <a href="http://dev.twitch.tv/" target="_blank">Twitch</a>

##App
<img src="/static/img/vid.gif">

####Features
- Automatically assigns players to tables.
- Players are texted after they are assigned to a table.
- List of all players is populated in left side bar, and names are grayed out once they have lost.
- Twitch stream and chat is embedded on page (optional).
- Challonge brackets appear in an iframe at the bottom of the page.

##Install Turni On Your Machine
Clone this repo:
```
git clone https://github.com/laurenor/Turni.git
```

Create and activate a virtual environment inside your project directory: 

```
virtualenv env

source env/bin/activate
```

Install the requirements:

```
pip install -r requirements.txt
```

***If psycopg2 is having issues installing, make sure that PostgreSQL's bin is added to the path*

Get your own secret keys for <a href="https://challonge.com/settings/developer" target="_blank">Challonge</a>.

Get your own secret keys for <a href="http://twilio.com" target="_blank">Twilio</a> and save them to a file `secrets.sh`. Your `secrets.sh` file should look something like this:

```
export CHALLONGE_API_KEY='YOURSECRETKEYIDHERE'
export TWILIO_NUMBER='YOURTWILIOPHONENUMBER'
export TWILIO_ACCOUNT_SID='YOURSECRETSIDHERE'
export TWILIO_AUTH_TOKEN='YOURSECRETAUTHTOKENHERE'
export TWILIO_TO_NUMBER='PARTICIPANTPHONENUMBERHERE'
```

#### Starting Up Your Server

Source your secret keys:

```
source secrets.sh
```

####Create a PostgreSQL Database or Restore Database

######Create a Database

```
createdb turnidb
```
p
Populate your database
```
python -i model.py
db.create_all()
exit()
```

#####Restore Database (use prepopulated data)
- Create database
```
createdb turnidb
```
- Import database dump
```
psql -f globals.sql
psql -f db-schema.sql turnidb
pg_restore -a -d turnidb -Fc full.dump
```

Run the app:

```
python server.py
```

Download and unzip <a href="https://ngrok.com/" target="_blank">ngrok</a> to create a secure tunnel to your localhost to allow Twilio access for voice routes.

Run ngrok:
```
./ngrok http 5000
```

Copy the new ngrok forwarding URL (`http://example.ngrok.io`) and update the <a href="https://www.twilio.com/user/account/phone-numbers/incoming" target="_blank">request URL for your Twilio number</a>.

Navigate to `localhost:5000` 

###Sample Info to Enter to Create a Turni Page
####User Login:
Username: lencat
Password: helloworld
####Tournament Info:
1. Tournament name: Turni International 2015
2. Tournament url (Challonge URL): <a href="http://www.challonge.com/turni2015" target="_blank">turni2015</a>
3. Twitch stream: <a href="http://www.challonge.com/nakat973" target="_blank">http://www.twitch.tv/nakat973</a>

___
### About the Developer
Turni was developed by <a href="http://www.github.com/laurenor" target="_blank">Lauren Ortencio</a>, a UCLA graduate and avid esports fan (Super Smash Bros. Melee / Smash4).  To learn more or connect with Lauren, send her a tweet <a href="http://twitter.com/lortencio" target="_blank">@LOrtencio</a> or a message on <a href="http://www.linkedin.com/in/laurenortencio" target="_blank">LinkedIn</a>. 
