from ecohabitat import db
from . import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(120), nullable = False)
    user_progress = db.relationship('UserProgress', backref='user', lazy=True)
    ongoing_challenges = db.relationship('Challenge', secondary='user_progress')
    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}',password='{self.password}',email='{self.email}' )"

class Challenge(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.Text(),nullable=False )
    description =   db.Column(db.Text() , nullable = False)
    duration = db.Column(db.Integer,nullable = False)
    points = db.Column(db.Float() , nullable = False )
    participants= db.relationship('User',backref = 'user_progress', lazy = True)



    def __repr__(self):
        return f"Challenge(id = '{self.id}' , name = '{self.name}' , description='{self.description}', duration='{self.duration}' , points='{self.points}')"

class UserProgress:
    id = db.Column(db.Integer,primary_key = False)
    start_date = db.Column(db.Date , nullable = False)
    end_date = db.Column(db.Date , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    challenge_id = db.Column(db.Integer , db.ForeignKey('challenge.id') , nullable = False)


    challenge = db.relationship("Challenge", backref="challenge")

    
    def __repr__(self):
        return f"UserProgress(id={self.id}, user_id={self.user_id}, challenge_id={self.challenge_id}, start_date='{self.start_date}', end_date={self.end_date})"