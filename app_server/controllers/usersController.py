from flask import (render_template, current_app, jsonify)

from werkzeug.security import generate_password_hash
import re
import jwt

from Models.model import register_post
from Models.model import login_post

from Models.model import update_put
from Models.model import update_get
from Models.model import update_delete


def registerController(request):
    # function used for Flask_D01 only (not used in API structure)
    if request.method == 'GET':
        return render_template('auth/register.html')

    elif request.method == 'POST':
        error = None
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not re.match("[^@]+@[^@]+\.[^@]+", email):
            error = 'Email is not correct'
        elif not password:
            error = 'Password is required.'

        if error is not None:
            return jsonify({'message': error}), 400
        else:
            return register_post(username, email, password)


def loginController(request):
    if request.method == 'GET':
        # function used for Flask_D01 only (not used in API structure)
        return render_template('auth/login.html')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return login_post(username, password)


def decode_auth_token(auth_token):
    try:
        checkId = jwt.decode(auth_token, current_app.config['SECRET_KEY'])
        return checkId['user_id']
    except jwt.ExpiredSignature:
        return 'Signature expired. Please login again'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please login again'


def userAdminController(request, id):
    auth_token = request.headers.get('x-access-token')
    check_id = decode_auth_token(auth_token)
    if id != check_id and id != 0:
        return jsonify({'message': 'Invalid token.'}), 400
    elif request.method == 'PUT':
        error = None
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not re.match("[^@]+@[^@]+\.[^@]+", email):
            error = 'Email is not correct'
        elif not password:
            error = 'Password is required.'

        if error is not None:
            return jsonify({'message': error}), 400
        else:
            return update_put(username, email, password, id)
    elif request.method == 'DELETE':
        return update_delete(id)
    elif request.method == 'GET':
        return update_get(id)
