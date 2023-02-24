from portfoliocraft import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

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

    __tablename__ = 'projects'
    

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text(255), nullable = False)
    screenshot = db.Column(db.String(255), nullable = False, default = 'default_screenshot.png')
    demo_link = db.Column(db.String(255), nullable = False)
    github_link = db.Column(db.String(255), nullable = False)

    users = db.relationship(User)
    

    def __init__(self, title, description, screenshot, demo_link, github_link, user_id):
        self.title = title
        self.description = description
        self.screenshot = screenshot
        self.demo_link = demo_link
        self.github_link = github_link
        self.user_id = user_id
    
    def __repr__(self):
        return f'Project ID: {self.id}, Title: {self.title}'

