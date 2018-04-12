# -*- coding: utf-8 -*-
"""
    admin.routes
    ~~~~~~~~~~~~

    Routes used for the admin panel of the application.
"""
import json
import os
from flask import abort, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from secrets import token_urlsafe
from werkzeug.utils import secure_filename

from app import db
from app.admin import bp
from app.admin.forms import ImportForm
from app.email import send_new_user_email
from app.models import User, Role


def upload_file(file):
    """
    Gets the file and filename from the form, makes sure it's secure, and
    saves it to the filesystem.

    :param file: <obj> file object containing the data
    :return: Path to file
    """
    f = file.data
    filename = secure_filename(f.filename)
    if not os.path.exists(current_app.config['IMPORT_FOLDER']):
        os.makedirs(current_app.config['IMPORT_FOLDER'])
    f.save(os.path.join(current_app.config['IMPORT_FOLDER'], filename))

    return os.path.join(current_app.config['IMPORT_FOLDER'], filename,)


def read_json(json_file, field=None):
    """
    Reads the imported json file.

    :param json_file: <str> The path to the json file
    :param field: <str> The field that is search for inside the
        json file, defaults to None
    :return: The json data read from the file
    """
    with open(json_file, 'r') as f:
        if field:
            try:
                data = json.load(f)[field]
            except KeyError:
                flash(f'Invalid file, missing key "{field}"')
                return redirect(url_for('admin'))
        else:
            data = json.load(f)

    return data


def import_users_to_db(data, mail_details=False):
    """
    When an admin uploads a json file with users, the users will be
    created in the database, a password will be generated, and finally
    the created account details will be send to the user by email.

    :param data: <str> Json data containing the user details
    :param mail_details: <bool> whether the users should receive a mail
        with their account credentials

    :return:
    """

    user_data = []
    for row in data:
        user = User(username=row['username'], email=row['email'])
        db.session.add(user)
        db.session.commit()

        r = Role.query.filter_by(role=row['role']).first()
        user.role_id = r.id
        db.session.commit()

        # Generate random initial password for imported user
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


@bp.route('/admin')
@login_required
def admin():
    if current_user.role.role != 'admin':
        abort(403)
    return render_template('admin/admin.html', title='Admin Panel')


@bp.route('/admin/users_import', methods=['GET', 'POST'])
@login_required
def import_users():
    user_import_form = ImportForm()
    if current_user.role.role != 'admin':
        abort(403)
    if user_import_form.validate_on_submit():
        file = upload_file(user_import_form.file)
        user_data = read_json(file, field='users')
        imported_users = import_users_to_db(user_data)
        if imported_users:
            flash('Imported Users (Copy to send to users)')
            for row in imported_users:
                flash(f'User: {row["username"]} ({row["email"]}) - '
                      f'Password: {row["password"]}')
        return redirect(url_for('admin.admin'))
    return render_template('admin/import_users.html', title='Admin Panel: Import Users',
                           user_import_form=user_import_form)


@bp.route('/admin/users_overview')
def users_overview():
    if current_user.role.role != 'admin':
        abort(403)
    users = User.query.all()
    return render_template('admin/users_overview.html', title='Users Overview',
                           users=users)
