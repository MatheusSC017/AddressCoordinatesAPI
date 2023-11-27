import os
from flask import Flask
from flask_restful import Api
from .app_setup import DATABASE, SECRET_KEY


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        DATABASE=DATABASE
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import routers
    routers.initialize_routes(api)

    return app
