import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

####################
## DATABASE SETUP ##
####################

#may need to come back to this if it isn't working
def connect_to_db(flask_app, db_uri="postgresql:///portfoliocraft", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

db = SQLAlchemy()
Migrate(app, db)


#########################
## LOGIN CONFIGURATIONS##
#########################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


##############################################################


from portfoliocraft.core.views import core
from portfoliocraft.error_pages.handlers import error_pages
from portfoliocraft.users.views import users

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)

