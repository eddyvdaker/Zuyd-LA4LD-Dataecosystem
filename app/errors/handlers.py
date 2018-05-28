from flask import render_template, request
from flask_babel import _

from app import db
from app.api.errors import error_response as api_error_response
from app.errors import bp


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
           request.accept_mimetypes['text/html']


@bp.app_errorhandler(403)
def forbidden_error(error):
    if wants_json_response():
        return api_error_response(403)
    return render_template(
        'errors/error.html', title=_('403 - Forbidden')
    ), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template(
        'errors/error.html', title=_('404 - File Not Found')
    ), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template(
        'errors/error.html', title=_('500 - Internal Server Error')
    ), 500
