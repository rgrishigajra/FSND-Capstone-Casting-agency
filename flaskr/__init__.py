from flask import Flask, request, jsonify, abort
from .database.models import setup_db, Actor, Movie, create_and_drop_all


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    # routes
    ''' sample route '''
    @app.route('/')
    def index():
        return jsonify({
            "success": True,
            "index_route": "For verifying presence"
        })

    return app


app = create_app()
