import httpx
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

import os
import requests

"""
Gets data from ELMS API calls

"""
class Elms:

    def __init__(self):
        # These variables will be kept in .env when setting up the script to run within our backend
        self.__token = os.getenv("elms_token")
        self.__current_term = os.getenv("current_term")
        self.__csv_destination = os.getenv("csv_destination")
        self.__quest_courses = ['BMGT490H', 'BMGT390H', 'BMGT190H', 'BMGT438A']
        self.__api_secret_key = os.getenv("api_secret_key")


    """
    Returns dict of class_name => class_id

    """
    def get_class_ids(self):
        r = httpx.get('https://canvas.instructure.com/api/v1/courses?per_page=20&{}'.format(self.__token))
        course_data = json.load(r)
        courses = {}

        # get course ids
        for x in course_data:
            name = x['name']
            if self.__current_term in name:
                id = str(x['id'])
                for course in self.__quest_courses:
                    if course in name:
                        courses[course] = id
        return courses


    """
    Returns list of student tuples (id, login_id, last_activity, current_grade) in a given course

    """
    def get_enrollments(self, course_id):
        r = httpx.get('https://canvas.instructure.com/api/v1/courses/{}/enrollments?per_page=60&{}'.format(course_id, self.__token))
        enroll_data = json.load(r)
        enrollments = []

        for x in enroll_data:
            if x['type'] == 'StudentEnrollment':
                user = x['user']
                grades = x['grades']

                # get full name
                name = (user['sortable_name'].split(", "))
                last_name = name[0]
                first_name = name[1]

                # canvas id used for api calls
                canvas_id = str(user['id'])
                directory_id = user['login_id']
                uid = user['sis_user_id']
                last_activity = x['last_activity_at']
                current_grade = grades['current_score']

                enroll = (canvas_id, first_name, last_name, uid, directory_id, last_activity, current_grade)
                enrollments.append(enroll)

        return enrollments


    """
    Returns percentage of late assignments for a given student in a given course

    """
    def get_late_assignments(self, course_id, student_id):
        r = httpx.get('https://canvas.instructure.com/api/v1/courses/{}/analytics/users/{}/assignments/?per_page=45&{}'.format(course_id, student_id, self.__token))
        assignment_data = json.load(r)
        total_assignments = len(assignment_data)
        num_late = 0

        for x in assignment_data:
            if x['status'] == 'late':
                num_late += 1

        percent_late = num_late/total_assignments
        return percent_late


    """
    Returns groups for a given course

    """
    def get_groups(self, course):
        r = httpx.get('https://canvas.instructure.com/api/v1/courses/{}/groups?per_page=20&{}'.format(course, self.__token))
        group_data = json.load(r)

        groups = {}
        for x in group_data:
            group_id = x['id']
            group_name = x['name']

            groups[group_id] = group_name

        return groups


    """
    Returns students in a given group

    """
    def get_students_in_group(self, group_id):
        r = httpx.get('https://canvas.instructure.com/api/v1/groups/{}/users?per_page=10&{}'.format(group_id, self.__token))
        member_data = json.load(r)
        memberships = []

        for x in member_data:
            user = x['sis_user_id']
            memberships.append(user)

        return memberships

    """
    Generate CSV of all ELMS student data
    **(This will most likely not be needed but we will keep for now before we know for sure)**
    """

    def generate_csv(self):
        courses = self.get_class_ids()
        students = {'directory_id': [], 'course': [], 'lastView': [], 'currentGrade': [], 'percentLate': []}

        # go through courses
        for name, course_id in courses.items():
            # go through students
            enrollments = e.get_enrollments(course_id)
            for student in enrollments:
                # construct student object for each student enrollment
                percent_late = e.get_late_assignments(course_id, student[0])
                students["directory_id"].append(student[4])
                students["course"].append(name)
                students["lastView"].append(student[5])
                students["currentGrade"].append(student[6] if not None else 0)
                students['percentLate'].append(percent_late)

        df = pd.DataFrame(students)
        df.to_csv(self.__csv_destination, index = False)

        # get auth token to post to db
        auth_url = 'http://valerian.cs.umd.edu:5000/auth?key={}&directoryId=aodentha'.format(self.__api_secret_key)
        auth_response = requests.get(auth_url)
        auth_token = auth_response.json()['access_token']

        # post to db
        hed = {'Authorization': 'Bearer ' + auth_token}
        post_url = 'http://valerian.cs.umd.edu:5000/elms?filePath={}'.format(self.__csv_destination)
        response = requests.post(post_url, headers=hed)

        print("done")


"""
###### DRIVER CODE

"""

e = Elms()
e.generate_csv()
