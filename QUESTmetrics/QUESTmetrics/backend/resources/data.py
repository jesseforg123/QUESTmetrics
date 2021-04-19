from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from utils.utils import addToParser, isUnique, admin_required
import json
from utils import errors
from app import tables

from app import db, studentTablesIgnorePopulate, groupTablesIgnorePopulate

class ClearResource(Resource):
    @admin_required
    def delete(self):
        db.session.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for tbl in tables:
            db.session.execute('TRUNCATE table {}'.format(tbl))
            db.session.commit()

        db.session.execute('SET FOREIGN_KEY_CHECKS = 1;')
        db.session.commit()
        return make_response('', 204)

class GroupBasedDataResource(Resource):
    @admin_required
    def get(self, name, table):
        if table not in groupTablesIgnorePopulate:
            return errors.NoTable()
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        response = db.session.execute('SELECT groupId FROM groups WHERE name = :name;', {'name':name})
        result = [dict(r) for r in response]
        groupId = result[0]['groupId']

        response = db.session.execute('SELECT * FROM {} WHERE groupId = :groupId;'.format(table), {'groupId':groupId})
        if response is None:
            return make_response(jsonify({'result' : ""}), 200)
        return make_response(jsonify([dict(r) for r in response]), 200)

class SlackResource(Resource):
    @admin_required
    def get(self):
        response = db.session.execute("SELECT * FROM slackData;")
        return make_response(jsonify([dict(r) for r in response]), 200)

    @admin_required
    def post(self, name):
        if isUnique('name', name, 'groups', db):
            return errors.NoGroup()

        response = db.session.execute('SELECT groupId FROM groups WHERE name = :name;', {'name':name})
        result = [dict(r) for r in response]
        groupId = result[0]['groupId']

        query = ''' LOAD DATA INFILE 'slack.csv'
                    INTO TABLE slackData
                    FIELDS TERMINATED BY ','
                    IGNORE 1 LINES
                    (slackMsgId, channel, user, timestamp)
                    SET groupID=:gid
                ;'''

        db.session.execute(query , {'gid' : groupId})
        db.session.commit()

        return make_response('', 204)


class ElmsResource(Resource):
    @admin_required
    def get(self):
        response = db.session.execute("SELECT * FROM elmsData;")
        return make_response(jsonify([dict(r) for r in response]), 200)

    @admin_required
    def post(self):
        query = ''' LOAD DATA INFILE 'elms_data.csv'
                    INTO TABLE elmsData
                    FIELDS TERMINATED BY ','
                    IGNORE 1 LINES
                    (@directory_id,@course,timestamp, lastView,currentGrade,percentLate)
                    SET studentId=(SELECT studentId FROM students JOIN people ON students.personId = people.personId AND directoryId=@directory_id),
                        classId=(SELECT classId FROM classes WHERE className=@course)
                ;'''

        db.session.execute(query)
        db.session.commit()

        return make_response('', 204)

class StudentBasedDataByUIDResource(Resource):
    @admin_required
    def get(self, table, uid, className):
        if not uid.isnumeric():
            return errors.NotNumeric()
        if isUnique('uid', uid, 'students', db):
            return errors.NoStudent()
        if table not in studentTablesIgnorePopulate:
            return errors.NoTable()
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()

        response = db.session.execute('SELECT * FROM students WHERE uid = :uid;', {'uid' : uid})
        result = [dict(r) for r in response]
        studentId = result[0]['studentId']

        response = db.session.execute('SELECT classId FROM classes WHERE className = :className;', {'className' : className})
        result = [dict(r) for r in response]
        classId = result[0]['classId']

        response = db.session.execute('SELECT * FROM {} WHERE classId = :cid AND studentId = :sid;'.format(table), {'cid':classId, 'sid':studentId})
        if response is None:
            return errors.NoStudent()

        return make_response(jsonify([dict(r) for r in response]), 200)


class StudentBasedDataByDirectoryIdResource(Resource):
    @admin_required
    def get(self, table, directoryId, className):
        if table not in studentTablesIgnorePopulate:
            return errors.NoTable
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()
        
        response = db.session.execute('SELECT * FROM people WHERE directoryId = :d;', {'d':directoryId})

        result = [dict(r) for r in response]
        personId = result[0]['personId']

        if isUnique('personId', personId, 'students', db):
            return errors.NoStudent()

        response = db.session.execute('SELECT studentId FROM students t1 JOIN people t2 ON t1.personId = t2.personId WHERE directoryId = :directoryId', {'directoryId' : directoryId})
        result = [dict(r) for r in response]
        studentId = result[0]['studentId']

        response = db.session.execute('SELECT classId FROM classes WHERE className = :className;', {'className' : className})
        result = [dict(r) for r in response]
        classId = result[0]['classId']

        response = db.session.execute('SELECT * FROM {} WHERE classId = :cid AND studentId = :sid;'.format(table), {'cid':classId, 'sid':studentId})

        if response is None:
            return errors.NoStudent()
        return make_response(jsonify([dict(r) for r in response]), 200)
