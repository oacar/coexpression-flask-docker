import json
import os

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from app.results import orf, Results


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(os.environ["APP_SETTINGS"])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    api.add_resource(Results, "/results")
    api.add_resource(orf, "/orf_name/<string:orf_name>")
    from . import db

    db.init_app(app)

    return app
