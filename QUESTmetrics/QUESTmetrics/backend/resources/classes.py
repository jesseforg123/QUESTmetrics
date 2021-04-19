from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from utils.utils import addToParser, isUnique, admin_required
from utils import errors
import json

from app import db

class ClassResource(Resource):
    @jwt_required
    def get(self):
        response = db.session.execute('SELECT className FROM classes;')
        return make_response(json.dumps([dict(r) for r in response]), 200)

    @admin_required
    def post(self):
        if request.json is not None:
            return errors.InvalidBody()
        requiredArgs = ['className']

        parser = reqparse.RequestParser(bundle_errors=True)
        parser = addToParser(requiredArgs, parser, required=True)

        args = parser.parse_args()

        if not isUnique('className', args['className'], 'classes', db):
            return errors.DuplicateClass()

        # -- Add to Classes -- #
        query = '''
        INSERT INTO classes (className) VALUES (:n);
        '''
        db.session.execute(query, {
            'n':args['className'],
        })
        db.session.commit()

        response = db.session.execute('SELECT * FROM classes WHERE className = :n;',{'n':args['className']})
        
        # -- Create Survey -- #
        query = "INSERT INTO surveys (classId) VALUES (:c);"
        db.session.execute(query, {
            'c': [dict(r) for r in response][0]['classId']
        })

        db.session.commit()
        response = db.session.execute('SELECT * FROM classes WHERE className = :n;',{'n':args['className']})

        return make_response(json.dumps([dict(r) for r in response][0]), 200)

    @admin_required
    def delete(self):
        if request.json is not None:
            return errors.InvalidBody()
        # Delete a class from the classes table
        requiredArgs = ['className']
        parser = reqparse.RequestParser(bundle_errors=True)
        parser = addToParser(requiredArgs, parser, required=True)
        args = parser.parse_args()

        # Checks to see if a class with className exists.
        if isUnique('className', args['className'], 'classes', db):
            return errors.NoClass()
        
        #Delete from surveys
        query = """DELETE FROM surveys
        WHERE classId = (SELECT classId FROM classes WHERE className = :c);
        """
        response = db.session.execute(query, 
        {
            "c":args['className']
        })

        #Delete from survey History
        query = """DELETE FROM surveyHistory
        WHERE classId = (SELECT classId FROM classes WHERE className = :c);
        """
        response = db.session.execute(query, 
        {
            "c":args['className']
        })

        #Delete from teams
        query = "DELETE FROM student_teams WHERE groupId IN (SELECT groupId FROM groups WHERE classId=(SELECT classId FROM classes WHERE className=:cname));"
        db.session.execute(query, {'cname':args['className']})

        #Delete from groups and classes
        query= """DELETE FROM groups WHERE classId=(SELECT classId from classes WHERE className=:cname);
                    DELETE FROM classes WHERE className=:cname;
                """
        db.session.execute(query, {'cname':args['className']})

        db.session.commit()
        

        return make_response('', 204)

class ClassesByDirectoryIdResource(Resource):
    @jwt_required
    def get(self, directoryId):
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()

        response = db.session.execute('SELECT * FROM people WHERE directoryId = :d;', {'d':directoryId})

        result = [dict(r) for r in response]
        personId = result[0]['personId']

        if isUnique('personId', personId, 'students', db):
            return errors.NoStudent()
        
        query = """
        SELECT className FROM classes
        JOIN groups ON classes.classId = groups.classId
        JOIN student_teams ON groups.groupId = student_teams.groupId
        JOIN students ON student_teams.studentId = students.studentId
        WHERE students.personId = :p;
        """
        response = db.session.execute(query, {
            "p":personId
        })
        return make_response(json.dumps([dict(r) for r in response]), 200)
