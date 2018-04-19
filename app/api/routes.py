# -*- coding: utf-8 -*-
"""
    api.routes
    ~~~~~~~~~~

    The routes for the API blueprint, contains mostly a local version of the
    documentation
"""
from app.api import bp


@bp.route('/api/help')
def api_help():
    return 'test'
