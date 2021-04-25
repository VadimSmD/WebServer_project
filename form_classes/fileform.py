from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField, FileField
from flask_wtf import FlaskForm


class FileForm(FlaskForm):
    name = StringField('Имя получателя', validators=[DataRequired()])
    file = FileField('Отправляемый файл', validators=[DataRequired()])
    submit = SubmitField('Отправить')
