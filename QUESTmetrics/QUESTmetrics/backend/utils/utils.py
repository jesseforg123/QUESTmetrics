import utils.errors as errors
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def addToParser(items, parser, required = False):
    for item in items:
        parser.add_argument(item, help=invalidMessage(item), location=['json', 'form', 'args'], required=required)
    return parser

def invalidMessage(item):
    return "Invalid " + item + ". "

def isUnique(item, value, table, db):
    query = "SELECT {} FROM {} WHERE {} = :val".format(item, table, item)
    response = db.session.execute(query, {'val': value}).fetchone()

    return response is None or len(response) == 0

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        idy = get_jwt_identity()
        if idy['privilege'] != 'admin':
            return errors.NotAdmin()
        else:
            return fn(*args, **kwargs)
    return wrapper
