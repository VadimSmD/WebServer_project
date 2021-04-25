from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField, TextAreaField
from flask_wtf import FlaskForm


class EmailForm(FlaskForm):
    name = StringField('Имя получателя', validators=[DataRequired()])
    thema = StringField('Имя получателя', validators=[DataRequired()])
    text = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')
