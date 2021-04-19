import requests

import statistics

import datetime

from sklearn import preprocessing

import numpy as np

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from utils.utils import addToParser, isUnique, admin_required
from utils import errors
import json

from resources.students import (StudentResource, StudentByUIDResource, StudentByDirectoryIdResource, StudentGroupResource,
StudentByUIDGroupResource, StudentByDirectoryIdGroupResource)
from resources.classes import ClassResource, ClassesByDirectoryIdResource
from resources.groups import (GroupsByClassResource, GroupsByStudentUIDResource, GroupsByStudentDirectoryIdResource,
GroupResource, WatchResource, GroupHealthResource, GroupHealthScoreResource, GroupRedResource, GroupsWatchedResource)
from resources.data import GroupBasedDataResource, StudentBasedDataByUIDResource, StudentBasedDataByDirectoryIdResource, ClearResource, ElmsResource, SlackResource
from resources.weights import WeightsResource
from resources.survey import StudentResponseResource


from app import db
class Metrics(Resource):
    # gets a list of all the class names
    @admin_required
    def get_classes(self):
        response = ClassResource.get(self)
        classes_bytes = response.data
        classes_str = classes_bytes.decode('utf-8')
        classes = json.loads(classes_str)
        class_name = []
        for i in range(len(classes)):
            class_name.append(classes[i]["className"])
        return class_name

    # returns all the slack data for each group
    @admin_required
    def get_group_data(self, class_name):
        class_data = {'Group': [], 'Msgs': [], 'Grade':[], 'Late': [], 'Days': [], 'Survey': [], 'Msg_Distr': []}
        response = GroupsByClassResource.get(self, class_name)
        groups_bytes = response.data
        groups_str = groups_bytes.decode('utf-8')
        groups = json.loads(groups_str)
        for group in groups:
            name = group["name"]
            response = GroupBasedDataResource.get(self, "slackData", name)
            if response.status_code == 404:
                slack_file = []
            else:
                slack_bytes = response.data
                slack_str = slack_bytes.decode('utf-8')
                slack_file = json.loads(slack_str)
            # the number of messages each user in the group has sent
            msg_count = {'User': [], 'Count': [], 'Percent': []}
            #SLACK STUFF
            for i in range(len(slack_file)):
                if (slack_file[i]['user'] not in msg_count['User']):
                    msg_count['User'].append(slack_file[i]['user'])
                    msg_count['Count'].append(1)
                else:
                    j = msg_count['User'].index(slack_file[i]['user'])
                    msg_count['Count'][j] += 1


        ##### Distribution of msgs in group
            sum_msgs = sum(msg_count['Count'])

            if len(msg_count['Count']) == 0:
                avg_msg = 0
            else:
                avg_msg = sum_msgs/ len(msg_count['Count'])

            for i in range(len(msg_count['User'])):
                if (sum_msgs != 0):
                    msg_count['Percent'].append(msg_count['Count'][i]/sum_msgs)
                else:
                    msg_count['Percent'].append(0)
            sd_ind = 0
            if (len(msg_count['Percent']) > 1):
                sd_ind = statistics.stdev(msg_count['Percent'])

            student_health = []
            avg_student_health = 0
            for i in range(len(msg_count['User'])):
                if msg_count['Percent'][i] >= (1/len(msg_count['User'])):
                    student_health.append(3)
                elif (msg_count['Percent'][i] < (1/len(msg_count['User']) and (msg_count['Percent'][i] >= (1/len(msg_count['User']) - sd_ind)))):
                    student_health.append(2)
                elif (msg_count['Percent'][i]  <=  (1/len(msg_count['User']) - sd_ind)):
                    student_health.append(1)
            if (len(msg_count['User']) != 0):
                avg_student_health = sum(student_health)/len(msg_count['User'])


            if (name not in class_data['Group']):
                class_data['Group'].append(name)
                class_data['Msgs'].append(avg_msg)
                class_data['Msg_Distr'].append(avg_student_health)

        return class_data

    # returns a list of students in the group
    @admin_required
    def get_students_in_group(self, name):
        response = StudentGroupResource.get(self, name)

        students_bytes = response.data
        students_str = students_bytes.decode('utf-8')
        students = json.loads(students_str)
        return students

    # ELMS STUFF and SURVEY STUFF
    @admin_required
    def get_student_data(self, class_name, name):
        student_data = {'Student': [], 'Grade': [], 'Percent': [], 'Days': [], 'Survey': []}
        students = self.get_students_in_group(name)


        # goes thru each student
        for student in students:
            uid = student['uid']
            directoryId = student['directoryId']
            uid = str(uid)
            # stores elmsData for student based on uid
            response = StudentBasedDataByUIDResource.get(self, "elmsData", uid, class_name)
            if response.status_code == 404:
                stdt = []
            else:
                stdt_bytes = response.data
                stdt_str = stdt_bytes.decode('utf-8')
                stdt = json.loads(stdt_str)

            # stores surveyData for student based on directoryId

            response = StudentResponseResource.get(self, directoryId, class_name)
            if response.status_code == 404:
                survey = []
            else:
                survey_bytes = response.data
                survey_str = survey_bytes.decode('utf-8')
                survey = json.loads(survey_str)

            #LAST OPENED
            # calculates the number of days since opening class's ELMs page



            if stdt != []:

                last_open = datetime.datetime.strptime(stdt[0]['lastView'], '%Y-%m-%dT%H:%M:%S')
                time_since_last_open = datetime.datetime.now() - last_open
                num_days = time_since_last_open.days
                #SURVEY DATA
                sum_survey = 0
                survey_total = 0
                if survey != []:
                    for i in range(len(survey['results']['answers'])):
                        ans = survey['results']['answers'][i]
                        if ans != None and type(ans) == int:
                            sum_survey += int(ans)
                        survey_total += 5




                student_data['Student'].append(uid)
                student_data['Grade'].append(stdt[0]['currentGrade'])
                student_data['Percent'].append(1-stdt[0]['percentLate'])
                student_data['Days'].append(-1*num_days)
                if survey_total == 0:
                    student_data['Survey'].append(0)
                else:
                    student_data['Survey'].append((sum_survey/survey_total) * 100)



                return student_data

    @admin_required
    def put(self):
        classes = self.get_classes()
        for i in range(len(classes)):
            class_name = classes[i]
            class_data = self.get_group_data(class_name)
            null_group = []
            index = []
            null_data = 0
            for j in range(len(class_data['Group'])):
                name = class_data['Group'][j]

                student_data = self.get_student_data(class_name, name)
                if student_data != None:
                    avg_grade = sum(student_data['Grade'])/ len(student_data['Grade'])
                    avg_percent = sum(student_data['Percent'])/ len(student_data['Percent'])
                    avg_days = sum(student_data['Days'])/ len(student_data['Days'])
                    avg_survey_data = sum(student_data['Survey'])/ len(student_data['Survey'])
                    class_data['Grade'].append(avg_grade)
                    class_data['Late'].append(avg_percent)
                    class_data['Days'].append(avg_days)
                    class_data['Survey'].append(avg_survey_data)
                else:
                    null_group.append(name)
                    index.append(null_data)
                null_data+=1
            for found_group in null_group:
                for group in class_data['Group']:
                    for x in index:
                        if found_group == group:
                            class_data['Group'].pop(x)
                            class_data['Msgs'].pop(x)
                            class_data['Msg_Distr'].pop(x)



            response = WeightsResource.get(self)
            weights_bytes = response.data
            weights_str = weights_bytes.decode('utf-8')
            weights = json.loads(weights_str)

            #ACTUAL METRICS CALC
            if len(class_data['Grade']) == 0:
                avg_grade = 0
            else:
                avg_grade = (sum(class_data['Grade'])/ len(class_data['Grade'])) * (weights['grades']/100)
            if len(class_data['Late']) == 0:
                avg_percent = 0
            else:
                avg_percent = (sum(class_data['Late'])/ len(class_data['Late'])) * (weights['lateness']/100)
            if len(class_data['Days']) == 0:
                avg_days = 0
            else:
                avg_days = (sum(class_data['Days'])/ len(class_data['Days'])) * (weights['lastView']/100)
            if len(class_data['Survey']) == 0:
                avg_survey = 0
            else:
                avg_survey = (sum(class_data['Survey'])/ len(class_data['Survey']))* (weights['survey']/100)
            if len(class_data['Msg_Distr']) == 0:
                avg_msg_dist = 0
            else:
                avg_msg_dist = (sum(class_data['Msg_Distr'])/ len(class_data['Msg_Distr']))
            if len(class_data['Msgs']) == 0:
                avg_msg = 0
            else:
                avg_msg = ((sum(class_data['Msgs'])/ len(class_data['Msgs'])) + avg_msg_dist) * (weights['slack']/100)

            avg_total = avg_msg + avg_grade + avg_percent + avg_days + avg_survey

            if len(class_data['Msgs']) < 2 and len(class_data['Msg_Distr']) < 2:
                sd_msgs = 0
            elif len(class_data['Msgs']) < 2 and len(class_data['Msg_Distr']) >= 2:
                sd_msgs = (statistics.stdev(class_data['Msg_Distr'])) * (weights['slack']/100)
            elif len(class_data['Msgs']) >= 2 and len(class_data['Msg_Distr']) < 2:
                sd_msgs = (statistics.stdev(class_data['Msgs'])) * (weights['slack']/100)
            else:
                sd_msgs = (statistics.stdev(class_data['Msgs']) + statistics.stdev(class_data['Msg_Distr'])) * (weights['slack']/100)
            if len(class_data['Grade']) < 2:
                sd_grade = 0
            else:
                sd_grade = statistics.stdev(class_data['Grade']) * (weights['grades']/100)
            if len(class_data['Late']) < 2:
                sd_late = 0
            else:
                sd_late = statistics.stdev(class_data['Late']) * (weights['lateness']/100)
            if len(class_data['Days']) < 2:
                sd_days = 0
            else:
                sd_days = statistics.stdev(class_data['Days']) * (weights['lastView']/100)
            if len(class_data['Survey']) < 2:
                sd_survey = 0
            else:
                sd_survey = statistics.stdev(class_data['Survey']) * (weights['survey']/100)

            sd_total = sd_msgs + sd_grade + sd_late + sd_days + sd_survey

            group_score = []

            ## WEIGHTS

            for i in range(len(class_data['Group'])):
                name = class_data['Group'][i]
                group_total = ((class_data['Msgs'][i] + class_data['Msg_Distr'][i]) * weights['slack']/100) + (class_data['Grade'][i] * weights['grades']/100) + (class_data['Late'][i] * weights['lateness']/100) + (class_data['Days'][i] * weights['lastView']/100) + (class_data['Survey'][i] * weights['survey']/100)
                group_score.append(group_total)
                # GREEN: greater than the average

                if group_total >= avg_total:
                    db.session.execute("UPDATE groups SET groupHealth = :newVal WHERE name = :n;" , {'n' : name, 'newVal' : 3})
                    db.session.commit()

                # YELLOW: in between average - sd and average
                elif group_total < avg_total and (group_total >= avg_total - sd_total):
                    db.session.execute("UPDATE groups SET groupHealth = :newVal WHERE name = :n;" , {'n' : name, 'newVal' : 2})
                    db.session.commit()
                #RED: less than average -sd
                elif group_total <= avg_total - sd_total:
                    db.session.execute("UPDATE groups SET groupHealth = :newVal WHERE name = :n;" , {'n' : name, 'newVal' : 1})
                    db.session.commit()
            if len(group_score) != 0:
                group_score = preprocessing.minmax_scale(group_score, feature_range=(0, 1), axis=0, copy=True)
            else:
                group_score = 0

            for i in range(len(class_data['Group'])):
                name = class_data['Group'][i]
                gs = group_score[i]
                db.session.execute("UPDATE groups SET groupScore = :newVal WHERE name = :n;" , {'n' : name, 'newVal' : gs})
                db.session.commit()


        response = GroupResource.get(self)
        res_bytes = response.data
        res_str = res_bytes.decode('utf-8')
        response = json.loads(res_str)

        return make_response(json.dumps([dict(r) for r in response]), 200)

    
