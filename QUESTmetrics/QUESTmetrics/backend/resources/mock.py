from flask import request, jsonify, make_response
from flask_restful import Resource
from utils.utils import admin_required, isUnique
import json
import names
from random import randint

from app import db

class MockData(Resource):
    @admin_required
    def post(self):
        query = """
        SELECT * FROM people JOIN students ON people.personId = students.personId;
        """
        response = db.session.execute(query)
        result = [dict(r) for r in response]

        for row in result:
            if row['firstName'] != 'Collin' and row['firstName'] != 'Amy':
                #UPDATE PEOPLE
                
                firstName = names.get_first_name()
                lastName = names.get_last_name()
                directoryId = (firstName[0] + lastName).lower()
                while not isUnique('directoryId', directoryId, 'people', db):
                    firstName = names.get_first_name()
                    lastName = names.get_last_name()
                    directoryId = (firstName[0] + lastName).lower()


                personId = row['personId']

                query = """
                UPDATE people SET
                firstName = :f,
                lastName = :l,
                directoryId = :d
                WHERE personId = :p;
                """

                db.session.execute(query, {
                    "f":firstName,
                    "l":lastName,
                    "d":directoryId,
                    "p":personId
                })

                #UPDATE Students
                UID = ''.join(str(randint(0, 9)) for _ in range(9))
                while not isUnique('uid', UID, 'students', db):
                    UID = ''.join(str(randint(0, 9)) for _ in range(9))

                query = """
                UPDATE students SET
                uid = :u
                WHERE personId = :p;
                """

                db.session.execute(query, {
                    "u":UID,
                    "p":personId
                })

        query = """
        SELECT * FROM people JOIN students ON people.personId = students.personId;
        """
        response = db.session.execute(query)
        result = [dict(r) for r in response]

        db.session.commit()

        return make_response(json.dumps(result), 200)
        

