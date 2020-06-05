from flask import request, url_for
from models import Question


def view_question_dlc(*args, **kwargs):
    question_id = request.view_args['question_id']
    question = Question.get(question_id)
    return [{'text': question.name, 'url': url_for('question', question_id=question.id)}]


VOTE_SCHEMA = {
    "properties": {
        "imei": {"type": "string"},
        "option": {"type": "number"},
    }, "required": ["imei", "option"]
}
