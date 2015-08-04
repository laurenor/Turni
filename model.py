"""Models and database functions for Turni."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

##############################################################################
# Model definitions
class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False) # how to make this unique?
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    user_type = db.Column(db.String(11), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<User user_id=%s username=%s>" % (self.user_id, self.username)

class Station(db.Model):

    __tablename__ = 'stations'

    station_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    match_id = db.Column(db.Integer, nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'))
    

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<User user_id=%s username=%s>" % (self.user_id, self.username)

class Tournament(db.Model):

    __tablename__ = 'tournaments'

    tournament_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tournament_name = db.Column(db.String(20), nullable=False) 

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Tournament tournament_id=%s tournament_name=%s>" % (self.tournament_id, self.tournament_name)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///turni.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."