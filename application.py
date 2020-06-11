from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from flask_restful import Api
from flask_minify import minify
from flask import (Flask, render_template, flash,
                   redirect, url_for, jsonify)
from flask_login import (LoginManager, login_required,
                         login_user, logout_user, current_user,)


from models import db
from forms import LoginForm, QuestionForm, OptionForm
from utils import view_question_dlc
from api import QuestionListResource, VoteResource, QuestionDetailResource
from services import (check_user, get_user, create_question, get_question,
                      create_option, get_option, delete_option, check_object)

application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret-key'

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'
login_manager.login_message = 'É necessário autenticar-se para aceder ao sistema'
login_manager.login_message_category = "warning"

breadcrumbs = Breadcrumbs()
breadcrumbs.init_app(application)

mini = minify(html=True, js=True, cssless=True)
mini.init_app(application)


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id=user_id)


@application.route('/', methods=['get'])
@register_breadcrumb(application, '.', 'Sides')
def index():
    return redirect(url_for('questions'))


@application.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = check_user(email=email, password=password)
        if user is None:
            flash('Credenciais inválidas.', 'danger')
        else:
            login_user(user)
            flash('Entrou como {}.'.format(user.email), 'success')
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@application.route('/logout', methods=['get'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/questions', methods=['get'])
@login_required
@register_breadcrumb(application, '.questions', 'Questões')
def questions():
    questions = current_user.questions
    return render_template('questions.html', questions=questions)


@application.route('/questions/<int:question_id>', methods=['get'])
@login_required
@register_breadcrumb(application, '.questions.question_detail', '',
                     dynamic_list_constructor=view_question_dlc)
def question(question_id):
    question = get_question(question_id=question_id)
    check_object(question)
    return render_template('question.html', question=question)


@db.atomic()
@application.route('/questions/new', methods=['get', 'post'])
@login_required
@register_breadcrumb(application, '.questions.new_question', 'Nova')
def new_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = create_question(
            question=form.question.data, description=form.description.data, category=form.category.data)
        flash('Questão criada', 'success')
        return redirect(url_for('questions', id=question.id))
    return render_template('new_question.html', form=form)


@db.atomic()
@application.route('/questions/<int:question_id>/options/new', methods=['get', 'post'])
@login_required
@register_breadcrumb(application, '.questions.question_detail.new_option', 'Nova Opção')
def new_option(question_id):
    form = OptionForm()
    question = get_question(question_id=question_id)
    check_object(question)
    if form.validate_on_submit():
        create_option(option=form.option.data, question=question)
        flash('Opção criada', 'success')
        return redirect(url_for('new_option', question_id=question.id))
    return render_template('new_option.html', form=form, question_id=question_id)


@db.atomic()
@application.route('/options/<int:option_id>', methods=['post'])
@login_required
def remove_option(option_id):
    option = get_option(option_id)
    check_object(option)
    delete_option(option)
    flash('Opção eliminada com sucesso', 'success')
    return redirect(url_for('question', question_id=option.question.id))


@application.errorhandler(404)
def not_found(e):
    resp = jsonify(dict(error="not found"))
    resp.status_code = 404
    return resp


api = Api(application)
api.add_resource(QuestionListResource, '/api/questions')
api.add_resource(QuestionDetailResource, '/api/questions/<int:question_id>')
api.add_resource(VoteResource, '/api/vote')

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
