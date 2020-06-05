from flask import request, abort, jsonify
from flask_restful import Resource
from jsonschema import validate, ValidationError
from peewee import IntegrityError

from models import Question
from utils import VOTE_SCHEMA
from services import vote, get_option


class QuestionResource(Resource):
    def get(self):
        return [question.to_map() for question in Question.select()]


class VoteResource(Resource):
    def post(self):
        try:
            validate(instance=request.json, schema=VOTE_SCHEMA)

            imei = request.json['imei']
            option = get_option(option_id=request.json['option'])

            if option is None:
                return make_response('Option not found')

            vote(imei=imei, option=option.id)
            return "Sucesso."
        except ValidationError as e:
            return make_response(e.message)
        except IntegrityError as e:
            return make_response('You already voted')


def make_response(msg):
    resp = jsonify(dict(error=msg))
    resp.status_code = 404
    return resp
