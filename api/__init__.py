import os
import logging

from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate
# from flask_session import Session
from flask_jwt_extended import JWTManager
from sqlalchemy_utils import create_database, database_exists

from api.config import config


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


def create_app(test_config=None):
    app = Flask(__name__)

    app.secret_key = 'super secret key'
    CORS(app)  # add CORS

    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")
    # for configuration options, look at api/config.py
    if test_config:
        app.config.from_mapping(**test_config)
    else:
        app.config.from_object(config[env])

    if env != "prod":
        db_url = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_exists(db_url):
            create_database(db_url)

    jwt = JWTManager(app)

    # register sqlalchemy to this app
    from api.models import db
    db.init_app(app)
    Migrate(app, db)

    # import and register blueprints
    from api.views import funcs
    for func in funcs:
        func(app)

    return app
