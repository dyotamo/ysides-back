from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired

_REQUIRED = DataRequired(message="Este campo é obrigatório.")
_CATEGORIES = [('COVID-19', 'COVID-19'), ('Outros', 'Outros'), ('Educação', 'Educação'), ('Saúde',
                                                                                          'Saúde'), ('Política', 'Política'), ('Sociedade', 'Sociedade'), ('Tecnologias', 'Tecnologias')]


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[_REQUIRED])
    password = PasswordField('Senha', validators=[_REQUIRED])


class QuestionForm(FlaskForm):
    question = TextField('Pergunta', validators=[_REQUIRED])
    description = TextAreaField('Descrição', validators=[])
    category = SelectField(
        'Categoria',
        choices=_CATEGORIES
    )


class OptionForm(FlaskForm):
    option = TextField('Opção', validators=[_REQUIRED])
