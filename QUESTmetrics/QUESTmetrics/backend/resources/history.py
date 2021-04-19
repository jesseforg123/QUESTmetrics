from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from utils.utils import addToParser, isUnique, admin_required
from utils import errors
import json

from app import db

class HistoryAllResource(Resource):
    @admin_required
    def get(self):
        query = """
        SELECT className, CAST(timestamp AS CHAR) as harvestedOn, data as results FROM surveyHistory
        JOIN classes ON classes.classId = surveyHistory.classId; 
        """
        response = db.session.execute(query)

        result = [dict(r) for r in response]
        for row in result:
            row['results'] = json.loads(row['results'])
        return make_response(json.dumps(result, sort_keys=True), 200)
    
    @admin_required
    def delete(self):
        query = """
        DELETE FROM surveyHistory;
        """
        response = db.session.execute(query)
        db.session.commit()
        return make_response('', 204)

class HistoryByClassResource(Resource):
    @admin_required
    def get(self, className):
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()

        # Select Class Id
        response = db.session.execute('SELECT classId FROM classes WHERE className = :n;',{'n': className})
        classId = [dict(r) for r in response][0]['classId']

        query = """
        SELECT className, CAST(timestamp AS CHAR) as harvestedOn, data as results FROM surveyHistory 
        JOIN classes ON classes.classId = surveyHistory.classId
        WHERE classes.classId = :c; 
        """
        response = db.session.execute(query, {
            "c":classId
        })

        result = [dict(r) for r in response]
        for row in result:
            row['results'] = json.loads(row['results'])
        return make_response(json.dumps(result, sort_keys=True), 200)
    
    @admin_required
    def delete(self, className):
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()

        # Select Class Id
        response = db.session.execute('SELECT classId FROM classes WHERE className = :n;',{'n': className})
        classId = [dict(r) for r in response][0]['classId']

        query = """
        DELETE FROM surveyHistory WHERE classId = :c;
        """
        response = db.session.execute(query, {
            "c":classId
        })
        db.session.commit()
        return make_response('', 204)