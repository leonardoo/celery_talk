from flask import Flask

from apps.controllers import register_blueprints
from apps.extensions import register_extensions
from apps.config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)

    return app
