"""Utility file to seed turni database =in seed_data/"""

from model import User, Station, Tournament, connect_to_db, db
from server import app

def load_users():
    """Load users from u.user into database."""
    users_file = open('./seed_data/u.user')
    for line in users_file:
        user_data = line.rstrip().split('|')
        individual_user = User(user_id=user_data[0], username=user_data[1], email=user_data[2], \
            password=user_data[3], user_type=user_data[4])
        db.session.add(individual_user)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    load_users()