from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from utils.utils import addToParser, isUnique, admin_required
from utils import errors
import json

from app import db

class GroupResource(Resource):
    @admin_required
    def get(self):
        # Get all groups
        response = db.session.execute('SELECT groupId, name, className, watch, groupHealth, groupScore FROM groups t1 JOIN classes t2 ON t1.classID = t2.classID;')
        return make_response(json.dumps([dict(r) for r in response]), 200)

    @admin_required
    def post(self):
        if request.json is not None:
            return errors.InvalidBody()
        # Add a group to the Groups table
        requiredArgs = ['name', 'className']
        parser = reqparse.RequestParser(bundle_errors=True)
        parser = addToParser(requiredArgs, parser, required=True)
        args = parser.parse_args()

        # -- Check Unique Constraints -- #
        if not isUnique('name', args['name'], 'groups', db):
            return errors.DuplicateGroup()

        if isUnique('className', args['className'], 'classes', db):
            return errors.NoClass()

        # -- Add group to table -- #
        query = 'INSERT INTO groups (name, classId) VALUES (:n, (SELECT classId FROM classes WHERE className=:cname));'

        db.session.execute(query, {
            'n': args['name'],
            'cname': args['className']
        })
        response = db.session.execute('SELECT groupId, name, className, watch, groupHealth, groupScore FROM groups t1 JOIN classes t2 ON t1.classID = t2.classID WHERE name = :n;',{'n':args['name']})
        db.session.commit()

        result = [dict(r) for r in response][0]

        return make_response(json.dumps(result), 200)

    @admin_required
    def delete(self):
        if request.json is not None:
            return errors.InvalidBody()
         # Delete a class from the classes table
        requiredArgs = ['name']
        parser = reqparse.RequestParser(bundle_errors=True)
        parser = addToParser(requiredArgs, parser, required=True)
        args = parser.parse_args()

        if isUnique('name', args['name'], 'groups', db):
            return errors.NoGroup()

        query = "DELETE FROM slackData WHERE groupId IN (SELECT groupId FROM groups WHERE name = :name);"
        db.session.execute(query, {'name':args['name']})

        query = "DELETE FROM student_teams WHERE groupId IN (SELECT groupId FROM groups WHERE name = :name);"
        db.session.execute(query, {'name':args['name']})

        query= "DELETE FROM groups WHERE name = :name;"
        db.session.execute(query, {'name':args['name']})
        db.session.commit()

        return make_response('', 204)

class WatchResource(Resource):
    @admin_required
    def get(self, name):
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        response = db.session.execute("SELECT * FROM groups WHERE name = :n;", {'n':name}).fetchone()

        return make_response(jsonify({'result':response['watch']}), 200)

    @admin_required
    def post(self, name):
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        response = db.session.execute("SELECT groupId, name, className, watch, groupHealth, groupScore FROM groups t1 JOIN classes t2 ON t1.classID = t2.classID WHERE name = :n;", {'n':name}).fetchone()

        currVal = response['watch']

        if currVal == 0:
            # Toggle
            db.session.execute("UPDATE groups SET watch = :newVal WHERE name = :n;" , {
                'n' : name,
                'newVal' : 1
            })
            # TODO: Some function that will notifiy this team they are being watched
        else:
            # Toggle
            db.session.execute("UPDATE groups SET watch = :newVal WHERE name = :n;" , {
                'n' : name,
                'newVal' : 0
            })
            # TODO: Some function that will notifiy this they are no longer being watched

        db.session.commit()
        return make_response('',204)

class GroupsWatchedResource(Resource):
    @admin_required
    def get(self):
        response = db.session.execute("SELECT groupId, name, className, watch, groupHealth, groupScore FROM groups t1 JOIN classes t2 ON t1.classID = t2.classID WHERE watch = 1;")

        result = [dict(r) for r in response]
        return make_response(json.dumps(result), 200)

class GroupsByClassResource(Resource):
    @admin_required
    def get(self, className):
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()

        response = db.session.execute("SELECT groupId, name, className, watch, groupHealth, groupScore FROM groups t1 JOIN classes t2 ON t1.classID = t2.classID WHERE className = :n;", {'n':className})
        return make_response(json.dumps([dict(r) for r in response]), 200)

class GroupHealthResource(Resource):
    @admin_required
    def get(self, name):
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        response = db.session.execute("SELECT * FROM groups WHERE name = :n;", {'n':name}).fetchone()
        return make_response(jsonify({'result': response['groupHealth']}), 200)

    @admin_required
    def put(self, name):
        if request.json is not None:
            return errors.InvalidBody()
        requiredArgs = ['groupHealth']
        parser = reqparse.RequestParser(bundle_errors=True)
        parser = addToParser(requiredArgs, parser, required = True)
        parser = addToParser(requiredArgs, parser)
        args = parser.parse_args()

        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        if not args['groupHealth'].isnumeric() or int(args['groupHealth']) > 3 or int(args['groupHealth']) < 1:
            return errors.InvalidHealth()

        db.session.execute("UPDATE groups SET groupHealth = :newVal WHERE name = :n;" , {'n' : name, 'newVal' : args['groupHealth']})
        db.session.commit()

        return make_response('', 204)

class GroupRedResource(Resource):
    @admin_required
    def get(self):
        response = db.session.execute("SELECT groupId, name, className, watch, groupHealth, groupScore FROM groups t1 JOIN classes t2 ON t1.classID = t2.classID WHERE groupHealth = 1;")
        return make_response(json.dumps([dict(r) for r in response]), 200)

class GroupsByStudentUIDResource(Resource):
    @admin_required
    def get(self, uid):
        if not uid.isnumeric():
            return errors.NotNumeric()
        if isUnique('uid', uid, 'students', db):
            return errors.NoStudent()

        response = db.session.execute('SELECT studentId FROM students WHERE uid = :uid', {'uid':uid})

        result = [dict(r) for r in response]
        studentId = result[0]['studentId']

        response = db.session.execute('''
        SELECT groups.groupId, groups.name, classes.className, groups.watch, groups.groupHealth  groups.groupScore FROM groups
        JOIN student_teams ON groups.groupId = student_teams.groupId
        JOIN classes ON groups.classId = classes.classId
        WHERE student_teams.studentId = :sid;
        ''', {
            'sid':studentId
        })
        return make_response(json.dumps([dict(r) for r in response]), 200)

class GroupsByStudentDirectoryIdResource(Resource):
    @admin_required
    def get(self, directoryId):
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()

        response = db.session.execute('SELECT * FROM people WHERE directoryId = :d;', {'d':directoryId})

        result = [dict(r) for r in response]
        personId = result[0]['personId']

        if isUnique('personId', personId, 'students', db):
            return errors.NoStudent()

        response = db.session.execute('SELECT studentId FROM students t1 JOIN people t2 ON t1.personId = t2.personId WHERE directoryId = :directoryId', {'directoryId':directoryId})

        result = [dict(r) for r in response]
        studentId = result[0]['studentId']

        response = db.session.execute('''
        SELECT groups.groupId, groups.name, classes.className, groups.watch, groups.groupHealth, groups.groupScore FROM groups
        JOIN student_teams ON groups.groupId = student_teams.groupId
        JOIN classes ON groups.classId = classes.classId
        WHERE student_teams.studentId = :sid;
        ''', {
            'sid':studentId
        })
        return make_response(json.dumps([dict(r) for r in response]), 200)



class GroupHealthScoreResource(Resource):
    @admin_required
    def get(self, name):
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()
        response = db.session.execute("SELECT * FROM groups WHERE name = :n;", {'n':name}).fetchone()
        return make_response(jsonify({'result': response['groupScore']}), 200)

    @admin_required
    def put(self, name):
        print("hello")
        if request.json is not None:
            return errors.InvalidBody()

        requiredArgs = ['groupScore']
        parser = reqparse.RequestParser(bundle_errors=True)
        parser = addToParser(requiredArgs, parser, required = True)
        parser = addToParser(requiredArgs, parser)
        args = parser.parse_args()

        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        if float(args['groupScore']) > 1.0 or float(args['groupScore']) < 0.0:
            return errors.InvalidHealth()

        db.session.execute("UPDATE groups SET groupScore = :newVal WHERE name = :n;" , {'n' : name, 'newVal' : args['groupScore']})
        db.session.commit()

        return make_response('', 204)
