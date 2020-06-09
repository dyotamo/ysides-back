from flask import request, abort, jsonify
from flask_restful import Resource
from jsonschema import validate, ValidationError
from peewee import IntegrityError

from models import Question
from utils import VOTE_SCHEMA
from services import vote, get_option, get_questions, get_question


class QuestionListResource(Resource):
    def get(self):
        return [question.to_map() for question in get_questions()]


class QuestionDetailResource(Resource):
    def get(self, question_id):
        question = get_question(question_id)
        if question is None:
            abort(404)
        return question.to_map()


class VoteResource(Resource):
    def post(self):
        try:
            validate(instance=request.json, schema=VOTE_SCHEMA)

            imei = request.json['imei']
            option = get_option(option_id=request.json['option'])

            if option is None:
                return make_response('Option not found')

            return vote(imei=imei, option=option).to_map()
        except ValidationError as e:
            return make_response(e.message)
        except IntegrityError as e:
            return make_response('You already voted', status_code=401)


def make_response(msg, status_code=404):
    resp = jsonify(dict(error=msg))
    resp.status_code = status_code
    return resp
