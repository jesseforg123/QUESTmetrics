from flask import request, jsonify, make_response
import json

# -- 400 -- #
def DuplicateGroup(): return make_response(jsonify({"msg":"Group already exists."}), 400)
def DuplicateClass(): return make_response(jsonify({"msg":"Class already exists."}), 400)
def DuplicateDID(): return make_response(jsonify({"msg":"Directory ID already in use."}), 400)
def DuplicateUID(): return make_response(jsonify({"msg":"UID already in use."}), 400)
def NotNumeric(): return make_response(jsonify({"msg":"Given value is not numeric."}), 400)
def InvalidHealth(): return make_response(jsonify({"msg":"Group health is invalid. Must be a number such that (1: Red, 2: Yellow, 3: Green)"}), 400)
def AlreadyGrouped(): return make_response(jsonify({"msg":"Student is already part of the queried group."}), 400)
def MalformedJSON(): return make_response(jsonify({"msg":"JSON is malformed."}), 400)
def MalformedList(): return make_response(jsonify({"msg":"JSON must be a list."}), 400)
def UnevenLength(): return make_response(jsonify({"msg":"Question and answer lists are of uneven lengths."}), 400)
def InvalidBody(): return make_response(jsonify({"msg": "Request body invalid. Clear body to make query-based requests."}), 400)

# -- 401 -- #
def InvalidSecret(): return make_response(jsonify({"msg":"Could not authorize. Queried secret is incorrect or has expired."}), 401)
def NoAuth(): return make_response(jsonify({"msg":"Could not authorize. Requested directoryId is either not a student in QUEST or not recognized as an administrator."}), 401)
def NotAdmin(): return make_response(jsonify({"msg":"Not authorzied. You must be an administrator to use this endpoint."}), 401)

# -- 404 -- #
def NoClass(): return make_response(jsonify({"msg":"Class could not be found."}), 404)
def NoStudent(): return make_response(jsonify({"msg":"Student could not be found with queried attributes."}), 404)
def NoGroup(): return make_response(jsonify({"msg":"Group could not be found."}), 404)
def NoPerson(): return make_response(jsonify({"msg":"Person could not be found."}), 404)
def NoTable(): return make_response(jsonify({"msg":"Table could not be found."}), 404)