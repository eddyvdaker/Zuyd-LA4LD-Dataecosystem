# -*- coding: utf-8 -*-
"""
    admin.routes
    ~~~~~~~~~~~~

    Routes used for the admin panel of the application.
"""
import json
import os
from datetime import datetime
from flask import abort, current_app, flash, redirect, render_template, \
    request, url_for
from flask_login import current_user, login_required
from secrets import token_urlsafe
from werkzeug.utils import secure_filename

from app import db
from app.admin import bp
from app.admin.forms import ImportForm, EditUserForm, EditModuleForm
from app.email import send_new_user_email
from app.models import User, Grade, Module, Result, Role


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
    Writes the data from from the json file to the db

    :param data: <dict> Json data containing the user details
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


def import_modules_to_db(data):
    """
    Writes the module data from the json file to the db.

    :param data: <dict> Dictionary containing the module data
    :return: Number of imported modules
    """
    for row in data:
        module = Module(
            code=row['code'],
            name=row['name'],
            description=row['description'],
            start=datetime.strptime(row['start'], '%Y-%m-%d'),
            end=datetime.strptime(row['end'], '%Y-%m-%d'),
            faculty=row['faculty']
        )
        db.session.add(module)
        db.session.commit()

    return len(data)


def import_results_to_db(data):
    """
    Writes the results data from the json file to the db

    :param data: <dict> Dictionary containing results data
    :return: Number of imported results
    """
    for row in data:
        user = User.query.filter_by(username=row['username']).first()
        module = Module.query.filter_by(code='tm01').order_by(
            Module.start.desc()).first()
        r = Result(identifier=user.hash_identifier(), module=module.id)
        db.session.add(r)
        db.session.commit()

        for grade in row['grades']:
            g = Grade(name=grade['name'], score=grade['score'],
                      weight=grade['weight'], result=r.id)
            db.session.add(g)
            db.session.commit()

    return len(data)


@bp.route('/admin')
@login_required
def admin():
    if current_user.role.role != 'admin':
        abort(403)
    return render_template('admin/admin.html', title='Admin Panel')


@bp.route('/admin/users_import', methods=['GET', 'POST'])
@login_required
def import_users():
    form = ImportForm()
    if current_user.role.role != 'admin':
        abort(403)
    if form.validate_on_submit():
        file = upload_file(form.file)
        user_data = read_json(file, field='users')
        imported_users = import_users_to_db(user_data)
        if imported_users:
            flash('Imported Users (Copy to send to users)')
            for row in imported_users:
                flash(f'User: {row["username"]} ({row["email"]}) - '
                      f'Password: {row["password"]}')
        return redirect(url_for('admin.admin'))
    return render_template('admin/import.html',
                           title='Admin Panel: Import Users',
                           form=form, example_gist_code=
                           'f73e48eea2c3672dec92adc2dd2627ef')


@bp.route('/admin/users_overview')
def users_overview():
    if current_user.role.role != 'admin':
        abort(403)
    users = User.query.all()
    return render_template('admin/users_overview.html',
                           title='Admin Panel: Users Overview',
                           users=users)


@bp.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    form = EditUserForm()
    if current_user.role.role != 'admin':
        abort(403)
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('The changes have been saved.')
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('admin/edit_user.html', form=form)


@bp.route('/admin/modules_import', methods=['GET', 'POST'])
def import_modules():
    form = ImportForm()
    if current_user.role.role != 'admin':
        abort(403)
    if form.validate_on_submit():
        file = upload_file(form.file)
        module_data = read_json(file, field='modules')
        import_status = import_modules_to_db(module_data)
        flash(f'{import_status} modules imported')
        return redirect(url_for('admin.admin'))
    return render_template('admin/import.html',
                           title='Admin Panel: Import Modules',
                           form=form, example_gist_code=
                           '3c1848ce491d9061fec9ae18ae5069e0')


@bp.route('/admin/modules_overview')
def modules_overview():
    if current_user.role.role != 'admin':
        abort(403)
    modules = Module.query.all()
    return render_template('admin/modules_overview.html',
                           title='Admin Panel: Modules Overview',
                           modules=modules)


@bp.route('/admin/edit_module/<module_id>', methods=['GET', 'POST'])
def edit_module(module_id):
    form = EditModuleForm()
    if current_user.role.role != 'admin':
        abort(403)
    module = Module.query.filter_by(id=module_id).first()
    if form.validate_on_submit():
        module.code = form.code.data
        module.name = form.description.data
        module.description = form.description.data
        module.start = form.start.data
        flash(f'start: {form.start.data}')
        module.end = form.end.data
        flash(f'end: {form.end.data}')
        module.faculty = form.faculty.data
        db.session.commit()
        flash('The changes have been saved.')
    elif request.method == 'GET':
        form.code.data = module.code
        form.name.data = module.name
        form.description.data = module.description
        form.start.data = module.start
        form.end.data = module.end
        form.faculty.data = module.faculty
    return render_template('admin/edit_module.html', form=form)


@bp.route('/admin/results_import', methods=['GET', 'POST'])
def import_results():
    form = ImportForm()
    if current_user.role.role != 'admin':
        abort(403)
    if form.validate_on_submit():
        file = upload_file(form.file)
        results_data = read_json(file, field='results')
        import_status = import_results_to_db(results_data)
        flash(f'{import_status} results imported')
        return redirect(url_for('admin.admin'))
    return render_template('admin/import.html',
                           title='Admin Panel: Import Results',
                           form=form, example_gist_code=
                           'd504fb80b48c28e2e1495e76ea33814e')
