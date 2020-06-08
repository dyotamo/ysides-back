from hashlib import md5
from flask_login import current_user

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


def create_user(email, password):
    Entity.create(email=email, password=generate_hash(password))


def create_question(question):
    return Question.create(name=question, entity=current_user.id)


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
    Vote.create(imei=imei, option=option)


def get_questions():
    return Question.select()
