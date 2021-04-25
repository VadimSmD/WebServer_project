from wtforms.validators import DataRequired
from wtforms import SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Войти')
