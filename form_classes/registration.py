from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm


class RegForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    password_rep = StringField('Repeat password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    cod = StringField('Code')
    submit = SubmitField('Войти')
