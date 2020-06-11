from hashlib import md5
from flask_login import current_user
from peewee import IntegrityError
from flask import abort

from models import Entity, Question, Option, Vote


def generate_hash(plain):
    return md5(plain.encode()).hexdigest()


def check_user(email, password):
    try:
        user = Entity.select().where(Entity.email == email).get()
        if user.password == generate_hash(password):
            return user
    except Entity.DoesNotExist:
        pass


def get_user(user_id):
    try:
        return Entity.get(user_id)
    except Entity.DoesNotExist:
        pass


def create_user(name, email, password):
    Entity.create(name=name, email=email, password=generate_hash(password))


def create_question(question, description, category):
    return Question.create(name=question, description=description, category=category, entity=current_user.id)


def get_question(question_id):
    try:
        return Question.get(question_id)
    except Question.DoesNotExist:
        pass


def create_option(option, question):
    return Option.create(name=option, question_id=question.id)


def get_option(option_id):
    try:
        return Option.get(option_id)
    except Option.DoesNotExist:
        pass


def vote(imei, option):
    last_vote = already_voted(imei=imei, option=option)

    if last_vote:
        delete_vote(last_vote)

    vote = Vote.create(imei=imei, option=option.id)
    return vote.option.question


def get_questions():
    return Question.select()


def already_voted(imei, option):
    '''
    Pega o voto, caso o IMEI já tenha votado na questão da opção
    '''
    for option in option.question.options:
        for vote in option.votes:
            if imei == vote.imei:
                return vote


def delete_option(option):
    option.delete_instance()


def delete_vote(vote):
    vote.delete_instance()


def check_object(obj):
    if obj is None:
        return abort(404)
