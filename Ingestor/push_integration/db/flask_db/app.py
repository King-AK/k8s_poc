from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(environment_config=None):
    app = Flask(__name__)
    app.config.from_object(environment_config)
    db.init_app(app)
    return app
