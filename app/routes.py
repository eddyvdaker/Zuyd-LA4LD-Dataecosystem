# -*- coding: utf-8 -*-
"""
    routes
    ~~~~~~

    Routes for the different parts of the data ecosystem.
"""
import os
import json
from flask import abort, flash, render_template, redirect, url_for, request, \
    send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from secrets import token_urlsafe
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse

from app import app, db
from app.email import send_new_user_email, send_password_reset_email
from app.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm,\
    ImportForm
from app.models import User, Role


@app.route('/')
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


@app.route('/profile')
@login_required
def profile():
    user_data = 'abc'
    return render_template('profile.html', title='Profile', data=user_data)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    if current_user.role.role != 'admin':
        abort(403)
    return send_from_directory(app.config['IMPORT_FOLDER'], filename)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin(imported_users=None):
    user_import_form = ImportForm()
    if current_user.role.role != 'admin':
        abort(403)

    def import_users(json_file, mail_details=False):
        """
        When an admin uploads a json file with users, the users will be
        created in the database, a password will be generated, and finally
        the created account details will be send to the user by email.

        :param json_file: <str> path to the json input file
        :param mail_details: <bool> whether the users should receive a mail
            with their account credentials

        :return:
        """
        file = os.path.join(app.config['IMPORT_FOLDER'], json_file)
        with open(file, 'r') as f:
            try:
                users = json.load(f)['users']
            except KeyError:
                flash('Invalid file, missing key "users".')
                return redirect(url_for('admin'))
        user_data = []
        for row in users:
            user = User(username=row['username'], email=row['email'])
            db.session.add(user)
            db.session.commit()

            r = Role.query.filter_by(role=row['role']).first()
            user.role_id = r.id
            db.session.commit()

            password = token_urlsafe()
            user.set_password(password)
            db.session.commit()

            new_user = {'username': user.username,
                        'password': password,
                        'email': user.email}

            if mail_details:
                if 'la4ld-test.com' not in user.email:
                    send_new_user_email(new_user)
            else:
                user_data.append(new_user)

        return user_data

    if user_import_form.validate_on_submit():
        f = user_import_form.file.data
        filename = secure_filename(f.filename)
        if not os.path.exists(app.config['IMPORT_FOLDER']):
            os.makedirs(app.config['IMPORT_FOLDER'])
        f.save(os.path.join(app.config['IMPORT_FOLDER'], filename))
        imported_users = import_users(
            os.path.join(app.config['IMPORT_FOLDER'], filename,),
            mail_details=False)
        if imported_users:
            flash('Imported Users (Copy to send to users)')
            for row in imported_users:
                flash(f'User: {row["username"]} ({row["email"]}) - '
                      f'Password: {row["password"]}')
        return redirect(url_for('admin'))

    return render_template('admin.html', title='Admin Panel',
                           user_import_form=user_import_form,)
