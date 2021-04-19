import flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

app = flask.Flask(__name__)

app.config.from_object('config')

# Enable CORS
cors = CORS(app)

# Create SQLAlchemy Instance
# https://www.sqlalchemy.org/
db = SQLAlchemy(app)

# Configure API from Flask RESTful for model routing
# https://flask-restful.readthedocs.io/en/latest/quickstart.html
api = Api(app)

# Configure for JWT
# https://flask-jwt-extended.readthedocs.io/en/stable/
jwt = JWTManager(app)

app.config['CORS_HEADERS'] = 'Content-Type'

studentTablesIgnorePopulate = ['elmsData']
groupTablesIgnorePopulate = ['slackData']
tables = ['slackData', 'elmsData', 'people', 'students', 'student_teams', 'classes', 'groups', 'weights', 'surveyHistory','surveys', 'questions', 'answers']