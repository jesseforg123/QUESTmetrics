from dotenv import load_dotenv
load_dotenv()

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_USERNAME = os.getenv('DB_USER')
DATABASE_PASSWORD = os.getenv('DB_PASS')
DATABASE_HOST = os.getenv('DB_HOST')
DATABASE_SCHEMA = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = 'mysql://' + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOST + '/' + DATABASE_SCHEMA
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_ENABLED     = True

CSRF_SESSION_KEY = "secret"

JWT_SECRET_KEY = 'katcBDCk0UhDDUjvfQxoaZNxFAwNZLZl'
