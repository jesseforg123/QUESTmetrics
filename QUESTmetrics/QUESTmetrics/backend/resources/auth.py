from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity
from utils.utils import addToParser, isUnique
from utils import errors
import json
import datetime

import os
from dotenv import load_dotenv
load_dotenv()

from app import db

class AuthResource(Resource):
    def get(self):
        if request.json is not None:
            return errors.InvalidBody()

        requiredArgs = ['key','directoryId']
        parser = reqparse.RequestParser(bundle_errors=False)
        parser = addToParser(requiredArgs, parser, required = True)
        args = parser.parse_args()

        if args['key'] != os.getenv('JWT_SECRET_KEY'):
            return errors.InvalidSecret()

        # ---- Admin Auth --- #
        response = db.session.execute("SELECT * FROM admin WHERE id = :did", {"did":args['directoryId']}).fetchone()
        if response is not None:
            priv = response['privileges']
            identity = {
                "directoryId":args['directoryId'],
                "privilege":priv
            }
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=identity, expires_delta=expires)
            return make_response(jsonify(access_token=access_token), 200)
        
        # ---- Student Auth ---- #
        if isUnique('directoryId', args['directoryId'], 'people', db):
            return errors.NoAuth()

        response = db.session.execute('SELECT * FROM people WHERE directoryId = :d;', {'d':args['directoryId']})
        result = [dict(r) for r in response]

        personId = result[0]['personId']

        if isUnique('personId', personId, 'students', db):
            return errors.NoAuth()
        
        priv = 'student'
        identity = {
            "directoryId":args['directoryId'],
            "privilege":priv
        }
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=identity, expires_delta=expires)
        return make_response(jsonify(access_token=access_token), 200)


