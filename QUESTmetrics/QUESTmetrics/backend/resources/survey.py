from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from utils.utils import addToParser, isUnique, admin_required
from utils import errors
import json

from app import db

class SurveyResource(Resource):
    @admin_required
    def get(self, className):
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()
            
        #Get Questions
        query ="""
        SELECT * FROM questions;
        """
        response = db.session.execute(query)
        result = [dict(r) for r in response]
        
        questions = []
        for questionObj in result:
            questions.append(questionObj['question'])
        
        #Gather Info
        query = """
        SELECT *
        FROM students JOIN people ON students.personId = people.personId
        JOIN student_teams ON students.studentId = student_teams.studentId
        JOIN groups ON student_teams.groupId = groups.groupId
        JOIN classes ON groups.classId = classes.classId
        WHERE classes.className = :c;
        """
        response = db.session.execute(query,{
            "c":className
        })

        result = [dict(r) for r in response]
        output = {}
        questions = output.update({"questions":questions})
        
        studentObjs = []

        for student in result:
            query = """
            SELECT *
            FROM surveys JOIN questions ON questions.surveyId = surveys.surveyId
            LEFT JOIN answers ON answers.questionId = questions.questionId
            WHERE surveys.classId = :c AND answers.studentId = :s; 
            """
            response = db.session.execute(query, {
                "c":student['classId'],
                "s":student['studentId']
            })

            answerObjs = [dict(r) for r in response]
            answerList = []
            for a in answerObjs:
                answerList.append(a['answer'])

            studentObjs.append({
                "answers":answerList,
                "firstName":student['firstName'],
                "lastName":student['lastName'],
                "uid":student['uid'],
                "className":student['className']
            })
        
        output.update({"results":studentObjs})

        return make_response(json.dumps(output), 200)



    @admin_required
    def post(self, className):
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()
        questions = request.json
        if not isinstance(questions, list):
            return errors.MalformedList()

        for questionObj in questions:
            if 'question' not in questionObj:
                return errors.MalformedJSON()

        # Select Class Id
        response = db.session.execute('SELECT classId FROM classes WHERE className = :n;',{'n': className})
        classId = [dict(r) for r in response][0]['classId']

        # Select Survey Id
        response = db.session.execute('SELECT surveyId FROM surveys WHERE classId = :classId;',{'classId': classId})
        surveyId = [dict(r) for r in response][0]['surveyId']

        # Post the Questions
        for questionObj in questions:
            questionString = questionObj['question']
            query = "INSERT INTO questions (surveyId, question) VALUES (:surveyId, :q);"
            db.session.execute(query, {
                "surveyId": surveyId,
                "q":questionString
            })
        db.session.commit()

        return make_response('', 204)
            

    @admin_required
    def delete(self, className):
        results = self.get(className).response
        results = list(map(lambda result: result.decode('utf-8'), results))
        
        query = """SELECT * FROM classes WHERE className = :c;
        """
        response = db.session.execute(query,{
            "c":className
        })
        result = [dict(r) for r in response]
        classId = result[0]['classId']

        query = """SELECT * FROM surveys
        WHERE classId = :c;
        """
        response = db.session.execute(query, 
        {
            "c":classId
        })
        result = [dict(r) for r in response]
        surveyId = result[0]['surveyId']

        #Add to history
        query = "INSERT INTO surveyHistory (classId, data) VALUES (:c, :d)"
        db.session.execute(query, {
            "c":classId,
            "d":results
        })
        
        #Delete from current tables
        db.session.execute('SET FOREIGN_KEY_CHECKS = 0;')
        query = """DELETE questions, answers FROM 
        questions LEFT JOIN answers ON questions.questionId = answers.answerId
        WHERE surveyId = :s;
        """
        response = db.session.execute(query, 
        {
            "s":surveyId
        })
        db.session.execute('SET FOREIGN_KEY_CHECKS = 1;')

        db.session.commit()
        return make_response('', 204)


class StudentResponseResource(Resource):
    @admin_required
    def get(self, directoryId, className):
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()
        
        #Get Questions
        query ="""
        SELECT * FROM questions;
        """
        response = db.session.execute(query)
        result = [dict(r) for r in response]
        
        questions = []
        for questionObj in result:
            questions.append(questionObj['question'])
        
        #Gather Info
        query = """
        SELECT *
        FROM students JOIN people ON students.personId = people.personId
        JOIN student_teams ON students.studentId = student_teams.studentId
        JOIN groups ON student_teams.groupId = groups.groupId
        JOIN classes ON groups.classId = classes.classId
        WHERE classes.className = :c AND people.directoryId = :d;
        """
        response = db.session.execute(query,{
            "c":className,
            "d":directoryId
        })

        result = [dict(r) for r in response]
        if len(result) == 0:
            return errors.NoStudent()
        
        output = {}
        questions = output.update({"questions":questions})
        
        studentObjs = []

        for student in result:
            query = """
            SELECT *
            FROM surveys JOIN questions ON questions.surveyId = surveys.surveyId
            LEFT JOIN answers ON answers.questionId = questions.questionId
            WHERE surveys.classId = :c AND answers.studentId = :s; 
            """
            response = db.session.execute(query, {
                "c":student['classId'],
                "s":student['studentId']
            })

            answerObjs = [dict(r) for r in response]
            answerList = []
            for a in answerObjs:
                answerList.append(a['answer'])

            studentObjs.append({
                "answers":answerList,
                "firstName":student['firstName'],
                "lastName":student['lastName'],
                "uid":student['uid'],
                "className":student['className']
            })
        
        output.update({"results":studentObjs[0]})

        return make_response(json.dumps(output), 200)

    @jwt_required
    def put(self, directoryId, className):
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()
        if isUnique('directoryId', directoryId, 'people', db):
            return errors.NoPerson()

        #Class - student
        query = """
        SELECT * FROM people JOIN students ON people.personId = students.personId 
        JOIN student_teams ON students.studentId = student_teams.studentId
        JOIN groups ON student_teams.groupId = groups.groupId
        JOIN classes ON groups.classId = classes.classId
        JOIN surveys ON classes.classId = surveys.classId
        WHERE classes.className = :cn AND people.directoryId = :directoryId;
        """
        response = db.session.execute(query , {
            "cn": className,
            "directoryId" : directoryId
        })

        result = [dict(r) for r in response]
        if len(result) == 0:
            return errors.NoStudent()

        studentId = result[0]['studentId']
        surveyId = result[0]['surveyId']

        # Questions for this Survey
        questionIds = []
        query = "SELECT * FROM questions WHERE surveyId = :s;"
        response = db.session.execute(query , {
            "s" : surveyId
        })
        questions = [dict(r) for r in response]

        for question in questions:
            questionIds.append(question['questionId'])

        #Gather answers
        answers = request.json
        if not isinstance(answers, list):
            return errors.MalformedList()

        answerList = []
        for answerObj in answers:
            if 'answer' not in answerObj:
                return errors.MalformedJSON()
            else:
                answerList.append(answerObj['answer'])
        
        if len(answerList) != len(questionIds):
            return errors.UnevenLength()
        
        #Check replace condition
        query = "SELECT * FROM answers JOIN questions ON answers.questionId = questions.questionId WHERE studentId = :s AND surveyId = :sid;"
        response = db.session.execute(query, {
                 "s": studentId,
                 "sid": surveyId
             }).fetchone()
        
        newAnswer = response is None or len(response) == 0 

        #Insert
        if newAnswer:
            for idx in range(len(answerList)):
                query = "INSERT INTO answers (studentId, questionId, answer) VALUES (:s, :q, :a);"
                db.session.execute(query, {
                    "s": studentId,
                    "q": questionIds[idx],
                    "a": answerList[idx]
                })
        else:
            for idx in range(len(answerList)):
                query = "UPDATE answers SET answer = :a WHERE studentId = :s AND questionId = :q;"
                db.session.execute(query, {
                    "s": studentId,
                    "q": questionIds[idx],
                    "a": answerList[idx]
                })

        db.session.commit()
        return make_response('', 204)

class QuestionResource(Resource):
    @admin_required
    def get(self, className):
        if isUnique('className', className, 'classes', db):
            return errors.NoClass()

        query ="""
        SELECT questions.surveyId, classes.className, question FROM questions
        JOIN surveys ON surveys.surveyId = questions.surveyId
        JOIN classes ON surveys.classId = classes.classId
        WHERE className = :c;
        """
        response = db.session.execute(query, {
            "c":className
        })
        result = [dict(r) for r in response]
        return make_response(json.dumps(result), 200)
