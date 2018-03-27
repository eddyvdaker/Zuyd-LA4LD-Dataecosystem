# -*- coding: utf-8 -*-
"""
    la4ld
    ~~~~~

    A learning analytics for learning design data ecosystem build using Flask.
"""

from flask import Flask

from config import Config

TDD_TEST_ENV = ''


def create_app(config_class=Config):
    global TDD_TEST_ENV
    app = Flask(__name__)
    app.config.from_object(config_class)
    TDD_TEST_ENV = app.config['TDD_TEST_ENV']

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
