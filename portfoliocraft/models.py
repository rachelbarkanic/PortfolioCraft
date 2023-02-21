from portfoliocraft import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    profile_image = db.Column(db.String(255), nullable = False, default = 'default_profile.png')
    first_name = db.Column(db.String(255), nullable = False, index=True)
    last_name = db.Column(db.String(255), nullable = False, index=True)
    username = db.Column(db.String(255), unique = True, nullable = False, index=True)
    email = db.Column(db.String(255), unique = True, nullable = False, index=True)
    password_hash = db.Column(db.String(255), nullable = False)

    projects = db.relationship('Project', backref = 'author', lazy = True)


    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Username {self.username}'

class Project(db.Model):
    pass