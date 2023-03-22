from core import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# Models for the app
# Run the file once to initiate the dabase (creates steamapp.sqllite file)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)


class SteamProfiles(db.Model):
    rec_id = db.Column(db.Integer, primary_key=True)
    steam_username = db.Column(db.String(50), nullable=True)
    hours_in_2_weeks = db.Column(db.Integer)
    steam_profile_pic = db.Column(db.String(500))
    steam_profile_id = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

if __name__  == '__main__':
    with app.app_context():
        db.create_all()