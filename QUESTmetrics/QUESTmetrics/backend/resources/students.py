from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from utils.utils import addToParser, isUnique, admin_required
from utils import errors
import json

from app import db

class StudentResource(Resource):
    @admin_required
    def get(self):
        # Get all students as a JOIN on Person and Student
        response = db.session.execute('SELECT studentId, firstName, lastName, directoryId, uid FROM people t1 JOIN students t2 ON t1.personId = t2.personID;')
        return make_response(json.dumps([dict(r) for r in response]), 200)

    @admin_required
    def post(self):
        if request.json is not None:
            return errors.InvalidBody()
        requiredArgs = ['firstName', 'lastName', 'directoryId']
        nullableArgs = ['uid']

        parser = reqparse.RequestParser(bundle_errors=True)

        parser = addToParser(requiredArgs, parser, required = True)
        parser = addToParser(nullableArgs, parser)

        args = parser.parse_args()

        # -- Check Unique Constraints -- #
        if not isUnique('directoryId', args['directoryId'], 'people', db):
            return errors.DuplicateDID()

        if args['uid'] is not None and not isUnique('uid', args['uid'], 'students', db):
            return errors.DuplicateUID()

        # -- Add to People Table -- #
        query = '''
        INSERT INTO people (firstName, lastName, directoryId) VALUES (:fn,:ln,:d);
        '''

        db.session.execute(query, {
            'fn':args['firstName'],
            'ln':args['lastName'],
            'd':args['directoryId']
        })

        person = db.session.execute("SELECT * FROM people WHERE directoryId = :d;", {'d':args['directoryId']}).fetchone()
        personId = person['personId']

        # -- Add to Student Table -- #
        query = '''
        INSERT INTO students (uid, personId) VALUES (:uid,:pid);
        '''

        db.session.execute(query, {
            'uid':args['uid'],
            'pid':personId
        })

        # -- Return as a join of the 2 Tables -- #
        response = db.session.execute('SELECT studentId, firstName, lastName, directoryId, uid FROM people t1 JOIN students t2 ON t1.personId = t2.personID WHERE t1.directoryId = :d;',{'d':args['directoryId']})

        db.session.commit()

        return make_response(json.dumps([dict(r) for r in response][0]), 200)

class StudentByUIDResource(Resource):
    @admin_required
    def get(self, uid):
        if not uid.isnumeric():
            return errors.NotNumeric()
        if isUnique('uid', uid, 'students', db):
            return errors.NoStudent()

        # Get student with given UID as a JOIN on Person and Student
        response = db.session.execute('SELECT studentId, firstName, lastName, directoryId, uid FROM people t1 JOIN students t2 ON t1.personId = t2.personID WHERE t2.uid = :uid', {'uid':uid})

        result = [dict(r) for r in response]
        return make_response(json.dumps(result[0]), 200)

    @admin_required
    def delete(self, uid):
        if not uid.isnumeric():
            return errors.NotNumeric()
        if isUnique('uid', uid, 'students', db):
            return errors.NoStudent()
        
        resp = db.session.execute('SELECT * FROM students WHERE uid=:uid;', {'uid': uid})
        result = [dict(r) for r in resp]

        
        # Must get personId from person table to query student table
        query = '''
        DELETE FROM student_teams WHERE studentId=(SELECT studentId FROM students WHERE uid=:uid);
        DELETE FROM elmsData WHERE studentId=(SELECT studentId FROM students WHERE uid=:uid);
        DELETE FROM answers WHERE studentId=(SELECT studentId FROM students WHERE uid=:uid);
        DELETE FROM students WHERE uid=:uid; '''
        db.session.execute(query, {'uid':uid})

        db.session.commit()

        return make_response('', 204)



class StudentByDirectoryIdResource(Resource):
    @admin_required
    def get(self, directoryId):
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()
        # Get student with given UID as a JOIN on Person and Student
        response = db.session.execute('SELECT * FROM people WHERE directoryId = :d;', {'d':directoryId})
        result = [dict(r) for r in response]

        personId = result[0]['personId']

        if isUnique('personId', personId, 'students', db):
            return errors.NoStudent()

        response = db.session.execute('SELECT studentId, firstName, lastName, directoryId, uid FROM people t1 JOIN students t2 ON t1.personId = t2.personID WHERE t1.directoryId = :d;', {'d':directoryId})
        result = [dict(r) for r in response]
        
        return make_response(json.dumps(result[0]), 200)

    @admin_required
    def post(self, directoryId):
        if request.json is not None:
            return errors.InvalidBody()
        nullableArgs = ['uid']

        parser = reqparse.RequestParser(bundle_errors=True)
        parser = addToParser(nullableArgs, parser)

        args = parser.parse_args()

        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()

        if args['uid'] is not None and not isUnique('uid', args['uid'], 'students', db):
            return errors.DuplicateUID()
        
        if args['uid'] is not None and not args['uid'].isnumeric():
            return errors.NotNumeric()

        person = db.session.execute("SELECT * FROM people WHERE directoryId = :did;", {'did':directoryId}).fetchone()
        personId = person['personId']

        if not isUnique('personId', personId, 'students', db):
            return errors.DuplicateDID()

        query = "INSERT INTO students (uid, personId) VALUES (:uid, :personId);"
        db.session.execute(query, {
            'uid': args['uid'],
            'personId' : personId
        })
        db.session.commit()

        response = db.session.execute('SELECT studentId, firstName, lastName, directoryId, uid FROM people t1 JOIN students t2 ON t1.personId = t2.personID WHERE t1.directoryId = :d;',{'d':directoryId})

        return make_response(json.dumps([dict(r) for r in response][0]), 200)

    @admin_required
    def delete(self, directoryId):
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()

        response = db.session.execute('SELECT * FROM people WHERE directoryId = :d;', {'d':directoryId})
        result = [dict(r) for r in response]

        personId = result[0]['personId']

        if isUnique('personId', personId, 'students', db):
            return errors.NoStudent()

        query = '''DELETE FROM student_teams WHERE studentId=(SELECT studentId FROM students WHERE personId=(SELECT personId FROM people WHERE directoryId=:did));
                    DELETE FROM elmsData WHERE studentId=(SELECT studentId FROM students WHERE personId=(SELECT personId FROM people WHERE directoryId=:did));
                    DELETE FROM answers WHERE studentId=(SELECT studentId FROM students WHERE personId=(SELECT personId FROM people WHERE directoryId=:did));
                    DELETE FROM students WHERE personId=(SELECT personId from people WHERE directoryId=:did);'''
        db.session.execute(query, {'did':directoryId})

        db.session.commit()

        return make_response('', 204)

class StudentGroupResource(Resource):
    @admin_required
    def get(self, name):
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        response = db.session.execute("SELECT firstName, lastName, directoryId, uid FROM people INNER JOIN students ON people.personId = students.personID INNER JOIN student_teams ON students.studentId = student_teams.studentId INNER JOIN groups ON student_teams.groupId = groups.groupId WHERE name = :n;", {'n':name})
        result = [dict(r) for r in response]
        return make_response(json.dumps(result), 200)

class StudentByUIDGroupResource(Resource):
    @admin_required
    def post(self, uid, name):
        if not uid.isnumeric():
            return errors.NotNumeric()
        
        if isUnique('uid', uid, 'students', db):
            return errors.NoStudent()
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        # -- If student already part of group -- #
        getStudentGroupQuery = '''SELECT * FROM student_teams WHERE
                                    studentId=(SELECT studentId FROM students WHERE uid=:uid) AND
                                    groupId=(SELECT groupId FROM groups WHERE name=:n)
                                '''
        resp = db.session.execute(getStudentGroupQuery, {'uid': uid, 'n': name})

        if [dict(r) for r in resp]:
            return errors.AlreadyGrouped()

        # -- Insert -- #
        query = """INSERT INTO student_teams (studentId, groupId)
                    SELECT
                        (SELECT studentId FROM students WHERE uid=:uid),
                        (SELECT groupId FROM groups WHERE name=:n);"""

        db.session.execute(query, {'uid': uid, 'n': name})

        db.session.commit()
        resp = db.session.execute(getStudentGroupQuery, {'uid': uid, 'n': name})
        return make_response(json.dumps([dict(r) for r in resp][0]), 200)

    @admin_required
    def delete(self, uid, name):
        if not uid.isnumeric():
            return errors.NotNumeric()
        
        if isUnique('uid', uid, 'students', db):
            return errors.NoStudent()
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        student = db.session.execute("""SELECT * FROM student_teams WHERE
                                studentId=(SELECT studentId FROM students WHERE uid=:uid) AND
                                groupId=(SELECT groupId FROM groups WHERE name=:n)""", {'uid':uid, "n": name}).fetchone()

        if student is None:
            return errors.NoStudent()
        else: studentId = student['studentId']

        db.session.execute("""DELETE FROM student_teams WHERE
                                studentId=(SELECT studentId FROM students WHERE uid=:uid) AND
                                groupId=(SELECT groupId FROM groups WHERE name=:n)""", {'uid':uid, "n": name})

        db.session.commit()

        return make_response('', 204)

class StudentByDirectoryIdGroupResource(Resource):
    @admin_required
    def post(self, directoryId, name):
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        response = db.session.execute('SELECT * FROM people WHERE directoryId = :d;', {'d':directoryId})
        result = [dict(r) for r in response]

        personId = result[0]['personId']
        if isUnique('personId', personId, 'students', db):
            return errors.NoStudent()

        getStudentGroupQuery = '''SELECT * FROM student_teams WHERE
                                    studentId=(SELECT studentId FROM students WHERE personId=(SELECT personId from people WHERE directoryId=:directoryId)) AND
                                    groupId=(SELECT groupId FROM groups WHERE name=:n)
                                '''

        resp = db.session.execute(getStudentGroupQuery, {'directoryId': directoryId, 'n': name})
        if [dict(r) for r in resp]:
            return errors.AlreadyGrouped()

        query = """INSERT INTO student_teams (studentId, groupId)
                    SELECT
                        (SELECT studentId FROM students WHERE personId=(SELECT personId from people WHERE directoryId=:directoryId)),
                        (SELECT groupId FROM groups WHERE name=:n);"""

        db.session.execute(query, {'directoryId': directoryId, 'n': name})
        db.session.commit()
        resp = db.session.execute(getStudentGroupQuery, {'directoryId': directoryId, 'n': name})
        return make_response(json.dumps([dict(r) for r in resp][0]), 200)

    @admin_required
    def delete(self, directoryId, name):
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        response = db.session.execute('SELECT * FROM people WHERE directoryId = :d;', {'d':directoryId})
        result = [dict(r) for r in response]

        personId = result[0]['personId']

        if isUnique('personId', personId, 'students', db):
            return errors.NoStudent()
        
        student = db.session.execute("""SELECT studentId FROM student_teams WHERE
                                studentId=(SELECT studentId FROM students WHERE personId=(SELECT personId from people WHERE directoryId=:directoryId)) AND
                                groupId=(SELECT groupId FROM groups WHERE name=:n)""", {'directoryId':directoryId, "n": name}).fetchone()
        
        if student is None:
            return errors.NoStudent()
        else: studentId = student['studentId']

        db.session.execute("""DELETE FROM student_teams WHERE
                                studentId=(SELECT studentId FROM students WHERE personId=(SELECT personId from people WHERE directoryId=:directoryId)) AND
                                groupId=(SELECT groupId FROM groups WHERE name=:n)""", {'directoryId':directoryId, "n": name})

        db.session.commit()

        return make_response('', 204)
