from os import environ

from peewee import *
from flask_login import UserMixin
from dsnparse import parse_environ

if(environ.get('DATABASE_URL')):
    url = parse_environ('DATABASE_URL')
    db = PostgresqlDatabase(url.paths[0], user=url.username, password=url.password,
                            host=url.host, port=url.port)
else:
    db = SqliteDatabase('sides.db')


class Entity(Model, UserMixin):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    def to_map(self):
        m = self.__dict__['__data__']
        m.pop('password')
        return m

    class Meta:
        database = db


class Question(Model):
    name = CharField()
    description = CharField(max_length=500)
    entity = ForeignKeyField(Entity, backref='questions')

    def to_map(self, show_options=True):
        m = dict(self.__dict__['__data__'])
        m['entity'] = self.entity.to_map()
        m['options'] = [option.to_map()
                        for option in self.options] if show_options else None

        return m

    class Meta:
        database = db


class Option(Model):
    name = CharField()
    question = ForeignKeyField(Question, backref='options')

    def to_map(self):
        m = dict(self.__dict__['__data__'])
        m.pop('question')
        m['votes'] = self.votes.count()
        return m

    class Meta:
        database = db


class Vote(Model):
    imei = CharField()
    option = ForeignKeyField(Option, backref='votes')

    class Meta:
        database = db
        indexes = (
            (('imei', 'option'), True),)


if __name__ == "__main__":
    db.create_tables([Entity, Question, Option, Vote])
    from services import create_user

    create_user(name='Dássone J. Yotamo',
                email='dyotamo@gmail.com', password='admin')
