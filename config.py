# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration file for the la4ld application.
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    HASH_KEY = os.environ.get('HASH_KEY') or 'you-will-never-guess'
    TDD_TEST_ENV = os.environ.get('TDD_TEST_ENV') or \
                   'tdd-value-not-loaded-from-file'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['zuyd.la4ld.dataecosystem@gmail.com']
    IMPORT_FOLDER = os.environ.get('IMPORT_FOLDER') or '/tmp/la4ld/imports/'
    EXPORT_FOLDER = os.environ.get('EXPORT_FOLDER') or '/tmp/la4ld/exports/'
    FACT_STORE = os.environ.get('FACT_STORE') or \
                 os.path.join(basedir, 'fact-store.txt')
    LANGUAGES = ['en', 'nl']
    SYSTEM_ACCOUNT = os.environ.get('SYSTEM_ACCOUNT') or 'admin'
