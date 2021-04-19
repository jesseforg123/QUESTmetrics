from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from utils.utils import addToParser, isUnique, admin_required
from utils import errors
import json

from app import db

class WeightsResource(Resource):
    @admin_required
    def get(self):
        query = "SELECT slack, grades, lateness, survey, lastView FROM weights WHERE id = 'main';"
        response = db.session.execute(query)
        return make_response(json.dumps([dict(r) for r in response][0]), 200)

    @admin_required
    def put(self):
        if request.json is not None:
            return errors.InvalidBody()
        requiredArgs = ['slack', 'grades', 'lateness', 'survey', 'lastView']

        parser = reqparse.RequestParser(bundle_errors=True)
        parser = addToParser(requiredArgs, parser, required=True)

        args = parser.parse_args()

        for param in requiredArgs:
            if not args[param].replace('.','',1).isdigit():
                return errors.NotNumeric()

        query = """
        UPDATE weights SET
        slack = :slack,
        grades = :grades,
        lateness = :lateness,
        survey = :survey,
        lastView = :lastView
        WHERE id = 'main';
        """

        response = db.session.execute(query, {
            'slack':args['slack'],
            'grades':args['grades'],
            'lateness':args['lateness'],
            'survey':args['survey'],
            'lastView':args['lastView']
        })

        query = "SELECT slack, grades, lateness, survey, lastView FROM weights WHERE id = 'main';"
        response = db.session.execute(query)
        db.session.commit()
        return make_response(json.dumps([dict(r) for r in response][0]), 200)

    @admin_required
    def delete(self):
        query = """
        UPDATE weights SET
        slack = :slack,
        grades = :grades,
        lateness = :lateness,
        survey = :survey,
        lastView = :lastView
        WHERE id = 'main';
        """

        response = db.session.execute(query, {
            'slack': '20',
            'grades':'15',
            'lateness':'17.5',
            'survey':'30',
            'lastView':'17.5'
        })
        db.session.commit()

        return make_response('', 204)
