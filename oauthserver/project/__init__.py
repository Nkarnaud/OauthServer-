import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import app_config


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()


# App initialisation
def create_app(config_name):
    # instantiate the app
    app = Flask(__name__, instance_relative_config=True)
    # set config instance_relative_config=True
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)

    # register endpoints

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
