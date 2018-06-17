# -*- coding: utf-8 -*-
"""
    app.errors.handlers
    ~~~~~~~~~~~~~~~~~~~

    Handlers for different error messages
"""
from flask import render_template, request
from flask_babel import _

from app import db
from app.api.errors import error_response as api_error_response
from app.errors import bp


def wants_json_response():
    """Check if client ask for response in json format (for API)"""
    return request.accept_mimetypes['application/json'] >= \
           request.accept_mimetypes['text/html']


@bp.app_errorhandler(403)
def forbidden_error(error):
    """Handle 403 forbidden errors when user goes to page he/she is not allowed
    to browse to
    """
    if wants_json_response():
        return api_error_response(403)
    return render_template(
        'errors/error.html', title=_('403 - Forbidden')
    ), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    """Handle 404 file not found error when user goes to non-existent page"""
    if wants_json_response():
        return api_error_response(404)
    return render_template(
        'errors/error.html', title=_('404 - File Not Found')
    ), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 internal server error when an application error occures"""
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template(
        'errors/error.html', title=_('500 - Internal Server Error')
    ), 500
