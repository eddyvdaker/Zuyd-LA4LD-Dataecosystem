from flask import Blueprint

bp = Blueprint('xapi', __name__)

from app.xapi import routes
