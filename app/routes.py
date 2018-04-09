# -*- coding: utf-8 -*-
"""
    routes
    ~~~~~~

    Routes for the different parts of the data ecosystem.
"""
from flask import abort, render_template, send_from_directory
from flask_login import current_user, login_required

from app import app


@app.route('/')
def index():
    return render_template('index.html', title='Home Page')


@app.route('/error/test_500')
def error_test_500():
    abort(500)


@app.route('/profile')
@login_required
def profile():
    user_data = 'abc'
    return render_template('profile.html', title='Profile', data=user_data)


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    if current_user.role.role != 'admin':
        abort(403)
    return send_from_directory(app.config['IMPORT_FOLDER'], filename)


