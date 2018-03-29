# -*- coding: utf-8 -*-
"""
    routes
    ~~~~~~

    Routes for the different parts of the data ecosystem.
"""

from flask import abort, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/error/test_500')
def error_test_500():
    abort(500)


@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_data = None
    if str(user.username) == str(current_user.username):
        user_data = 'abc'

    test_data = f'user.username = {user.username}, current_user.username = {current_user.username}\n' \
                f'user.username == current_user.username : {user.username == current_user.username}'
    return render_template('profile.html', user=user, data=user_data, test_data=test_data)
