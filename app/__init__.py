from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session
import logging
from logging.handlers import RotatingFileHandler
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)  # necessaria per non avere errori a runtime quando si accede al form di login
db = SQLAlchemy(app)
migrate = Migrate(app,
                  db)  # migrate è una estensione che fornisce un’interazione tra Flask e Alembic, framework di migrazione per SQLAlchemy
login = LoginManager(app)  # inizializza il login
Session(app)
mail = Mail(app)

# log

if not app.debug:
    file_handler = RotatingFileHandler('logs/newspaper.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d] '
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Newspaper startup')

from app import routes, models, errors

# models definirà la struttura del database
