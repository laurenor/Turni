"""Models and database functions for Turni."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


##############################################################################
# Model definitions
class User(db.Model):

    __tablename__ = 'users'

    # need to change user_id to id
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False) # how to make this unique?
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    user_type = db.Column(db.String(11), nullable=False)
    phone = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<User user_id=%s username=%s>" % (self.user_id, self.username)

class Player(db.Model):

    __tablename__ = 'players'

    challonge_id = db.Column(db.Integer, primary_key=True)
    challonge_name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)

    @classmethod
    def add_to_db(cls, participant_data):
        """Parameter should be data from challonge api
        https://api.challonge.com/v1/tournaments/' + api_url + '/participants.json
        """

        for i in range(len(participant_data)):
            challonge_name = str(participant_data[i]['participant']['username'])
            if challonge_name is None:
                challonge_name = str(participant_data[i]['participant']['name'])
            challonge_id = int(participant_data[i]['participant']['id'])

            player = cls.query.filter_by(challonge_id=challonge_id).first()
            if not player:
                new_player = cls(challonge_name=challonge_name, challonge_id=challonge_id)
                db.session.add(new_player)
        db.session.commit()



    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Player challonge_id=%s challonge_name=%s>" % (self.challonge_id, self.challonge_name)

class Station(db.Model):

    __tablename__ = 'stations'

    station_id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'))  

    @classmethod
    def add_to_db(cls, max_stations, tournament):
        for i in range(max_stations):
            new_station = Station(station_id=i+1, tournament_id=tournament.tournament_id)
            db.session.add(new_station)
        db.session.commit()  

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Station station_id=%s>" % (self.station_id)

class StationPlayer(db.Model):

    __tablename__ = 'stations_players'

    stationplayer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'))
    challonge_id = db.Column(db.Integer, db.ForeignKey('players.challonge_id'))

    @classmethod
    def add_to_db(cls, match_data, open_stations):
        for i in range(len(match_data)):
            if match_data[i]['match']['state'] == 'open':
                cur_open_station = open_stations.pop(0)
                if cur_open_station:
                    new_station_player = StationPlayer(station_id=cur_open_station, challonge_id=match_data[i]['match']['player1_id'])
                    print new_station_player
                    new_station_player2 = StationPlayer(station_id=cur_open_station, challonge_id=match_data[i]['match']['player2_id'])
                    db.session.add(new_station_player)
                    db.session.add(new_station_player2)
        db.session.commit()

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<StationPlayer stationplayer_id=%s>" % (self.stationplayer_id)

class Tournament(db.Model):

    __tablename__ = 'tournaments'

    tournament_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tournament_name = db.Column(db.String(20), nullable=False) 
    max_stations = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Tournament tournament_id=%s tournament_name=%s>" % (self.tournament_id, self.tournament_name)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/turnidb'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."