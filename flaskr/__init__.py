import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, NotFound, PreconditionFailed
from flaskr.database.models import setup_db, Movie, Actor
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flaskr.auth.auth import AuthError, requires_auth
import sys
app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# ROUTES


# error handlers :
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(412)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 412,
        "message": "Precondition for resouce failed",
        "question": False
    }), 412


@app.errorhandler(404)
def error_resource_not_found(error):
    return jsonify({
        "success": False,
        "message": "Resource not found",
        "error": 404
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "message": "Internal server error",
        "error": 500
    }), 500


@app.errorhandler(422)
def not_processable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Request cant be processed"
    }), 422


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

@app.errorhandler(401)
def auth_error(error):
    return jsonify({
        "success":False,
        "error":401,
        "message":"Not Authorized"
    })
@app.errorhandler(403)
def auth_error(error):
    return jsonify({
        "success":False,
        "error":403,
        "message":"Forbidden"
    }),403
# @app.errorhandler(AuthError)
# def auth_error(error):
#     print(error)
#     return jsonify({
#         "success":False,
#         "error":error.status_code,
#         "message":error.error
#     }),error.status_code