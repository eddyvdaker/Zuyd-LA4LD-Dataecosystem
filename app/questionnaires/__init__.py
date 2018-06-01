from flask import Blueprint

bp = Blueprint('questionnaires', __name__)

from app.questionnaires import routes
