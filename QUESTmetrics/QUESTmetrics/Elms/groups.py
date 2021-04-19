import httpx
import json
import pandas as pd
from dotenv import load_dotenv
from elms_script import Elms
import requests

load_dotenv()

import os


"""
SCRIPT TO POPULATE GROUPS AND GROUP MEMBERS
"""

e = Elms()
courses = e.get_class_ids()


# get auth token to post to db
auth_url = 'http://valerian.cs.umd.edu:5000/auth?key={}&directoryId=aodentha'.format(self.__api_secret_key)
auth_response = requests.get(auth_url)
auth_token = auth_response.json()['access_token']
hed = {'Authorization': 'Bearer ' + auth_token}

for key, value in courses.items():
    groups = e.get_groups(value)
    for k, v in groups.items():

        # post groups
        group_url = 'http://valerian.cs.umd.edu:5000/groups?name={}&className={}&channel=channel'.format(v, key)
        resp = resp.post(group_url, headers=hed)
        print(resp)

        # post student memberships
        students = e.get_students_in_group(k)
        for s in students:
            item = {'uid': s, 'name': v}
            student_url = 'http://valerian.cs.umd.edu:5000/student/uid/{}/group/{}'.format(s, v)
            response = requests.post(student_url, headers=hed)
            print(response)
