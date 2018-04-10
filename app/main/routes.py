# -*- coding: utf-8 -*-
"""
    main.routes
    ~~~~~~~~~~~

    Routes that do not fit with any of the more specific blueprints or are
    core features of the application.
"""
from flask import abort, current_app, render_template, send_from_directory
from flask_login import current_user, login_required

from app.main import bp


@bp.route('/')
def index():
    return render_template('index.html', title='Home Page')


@bp.route('/error/test_500')
def error_test_500():
    abort(500)


@bp.route('/profile')
@login_required
def profile():
    user_data = 'abc'
    return render_template('profile.html', title='Profile', data=user_data)


@bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    if current_user.role.role != 'admin':
        abort(403)
    return send_from_directory(current_app.config['IMPORT_FOLDER'], filename)
