
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    screenshot = StringField('Add A URL For Your Screenshot', validators=[DataRequired()])
    demo_link = StringField('Demo Link', validators=[DataRequired()])
    github_link = StringField('Github Link', validators=[DataRequired()])
    submit = SubmitField('Add Your Project!')