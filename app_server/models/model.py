from flask import (jsonify, current_app)

from werkzeug.security import check_password_hash
import jwt
import datetime

from Config.db import get_db

# AUTHENTICATION FUNCTIONS


def register_post(username, email, password):
    db = get_db()
    error = None
    if db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
        error = 'User {} is already registered'.format(username)
    if error is None:
        db.execute(
            'INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
            (username, email, password)
        )
        db.commit()
        return jsonify({'message': 'user registered'}, 200)
    else:
        return jsonify({'message': error}), 400


def login_post(username, password):
    db = get_db()
    error = None
    user = db.execute('SELECT * FROM user WHERE username =?', (username,)).fetchone()

    if user is None:
        error = 'Username not found'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        token = jwt.encode({'user_id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(
            minutes=30)}, current_app.config['SECRET_KEY'])
        return jsonify([{'token': token.decode('UTF-8'), 'id': str(user['id'])}])
    else:
        return jsonify({'message': error}), 400

# USER_ADMIN FUNCTIONS


def update_get(id):
    if id == 0:
        users = get_db().execute('SELECT * FROM user')
        users = users.fetchall()
        rows = [dict(user) for user in users]
        return jsonify(rows)
    else:
        user = get_db().execute('SELECT id, username, email, password FROM user WHERE id = ?', (id,)).fetchone()
        if user is None:
            return jsonify({'message': 'User not found'}), 400
        else:
            row = [{'id': id, 'username': user['username'], 'email': user['email'], 'password': user['password']}]
            return jsonify(row), 200


def update_put(username, email, password, id):

    db = get_db()
    db.execute('UPDATE user SET username = ?, email = ?, password = ? WHERE id = ?', (username, email, password, id)
               )
    db.commit()
    return jsonify({'message': 'user updated'}), 200


def update_delete(id):
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'user deleted'}), 200

# ARTICLES MAIN FUNCTION


def articles_get(id):
    articles = get_db().execute('SELECT * FROM post')
    articles = articles.fetchall()
    rows = [dict(article) for article in articles]
    return jsonify(rows)


# ARTICLES ADMINISTRATION


def article_createPost(id, title, body):
    db = get_db()
    db.execute(
        'INSERT INTO post (user_id, title, body) VALUES (?, ?, ?)',
        (id, title, body)
    )
    db.commit()
    return jsonify({'message': 'article posted'}, 200)


def articles_adminGet(id):
    articles = get_db().execute('SELECT * FROM post WHERE user_id = ?', (id,))
    articles = articles.fetchall()
    rows = [dict(article) for article in articles]
    return jsonify(rows)


def articles_adminDelete(article_id):
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (article_id,))
    db.commit()
    return jsonify({'message': 'post deleted'}), 200
