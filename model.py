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
    phone = db.Column(db.String(11))

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<User user_id=%s username=%s>" % (self.user_id, self.username)

class Tournament(db.Model):

    __tablename__ = 'tournaments'

    tournament_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tournament_name = db.Column(db.String(20), nullable=False) 
    max_stations = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Tournament tournament_id=%s tournament_name=%s>" % (self.tournament_id, self.tournament_name)

class Match(db.Model):

    __tablename__ = 'matches'

    match_id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'))
    round_num = db.Column(db.Integer)
    player_1 = db.Column(db.String(20))
    player_2 = db.Column(db.String(20))

    def __repr__(self):
            """Provide helpful representation when printed"""
            return "<Match match_id=%s >" % (self.match_id)

class Position(db.Model):

    __tablename__ = 'positions'

    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'), primary_key=True)
    table_id = db.Column(db.String(10), primary_key=True)
    left = db.Column(db.String(10))
    top = db.Column(db.String(10))

    def __repr__(self):
            """Provide helpful representation when printed"""
            return "<Position tournament_id=%s table_id=%s >" % (self.tournament_id, self.table_id)



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