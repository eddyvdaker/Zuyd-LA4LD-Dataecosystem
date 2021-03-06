# -*- coding: utf-8 -*-
"""
    la4ld
    ~~~~~

    A learning analytics for learning design data ecosystem build using Flask.
"""

from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
babel = Babel()
bootstrap = Bootstrap()
cors = CORS()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)
    cors.init_app(app)

    # initialize blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.results import bp as results_bp
    app.register_blueprint(results_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.schedule import bp as schedule_bp
    app.register_blueprint(schedule_bp)

    from app.attendance import bp as attendance_bp
    app.register_blueprint(attendance_bp)

    from app.xapi import bp as xapi_bp
    app.register_blueprint(xapi_bp)

    from app.questionnaires import bp as questionnaires_bp
    app.register_blueprint(questionnaires_bp)

    # Setup logging
    if not app.debug and not app.testing:
        # Email logging
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])

            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()

            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='LA4LD Failure',
                credentials=auth, secure=secure)

            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # File logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/la4ld.log', maxBytes=2048000,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('LA4LD - Startup')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(
        current_app.config['LANGUAGES'])

from app import models
