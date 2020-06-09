from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

REQUIRED = DataRequired(message="Este campo é obrigatório.")


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[REQUIRED])
    password = PasswordField('Senha', validators=[REQUIRED])


class QuestionForm(FlaskForm):
    question = TextField('Pergunta', validators=[REQUIRED])
    description = TextField('Descrição', validators=[])


class OptionForm(FlaskForm):
    option = TextField('Opção', validators=[REQUIRED])
