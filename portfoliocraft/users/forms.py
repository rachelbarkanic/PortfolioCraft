from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from portfoliocraft.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message= 'Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Create User')

    def validate_email(self, email):
        if User.query.filter_by(email = self.email.data).first():
            raise ValidationError('This email is already being used, try another!')
    
    def validate_username(self, username):
        if User.query.filter_by(username = self.username.data).first():
            raise ValidationError('This username is already being used')



class UpdateUserForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update User Info')


    def validate_email(self, email):
        if User.query.filter_by(email = self.email.data).first():
            raise ValidationError('This email is already being used, try another!')
    
    def validate_username(self, username):
        if User.query.filter_by(username = self.username.data).first():
            raise ValidationError('This username is already being used, try again!')


######## NEED PROJECT FORM #########