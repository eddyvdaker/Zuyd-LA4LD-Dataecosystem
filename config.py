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
    TDD_TEST_ENV = os.environ.get('TDD_TEST_ENV') or 'tdd-value-not-loaded-from-file'

