from flask import jsonify
from .usersController import decode_auth_token

from Models.model import (articles_get, article_createPost, articles_adminGet, articles_adminDelete)


def articlesController(request, id):
    auth_token = request.headers.get('x-access-token')
    check_id = decode_auth_token(auth_token)
    if id != check_id:
        return jsonify({'message': 'Invalid token.'}), 400
    elif request.method == 'GET':
        return articles_get(id)


def articleCreateController(request, id):
    auth_token = request.headers.get('x-access-token')
    check_id = decode_auth_token(auth_token)
    if id != check_id:
        return jsonify({'message': 'Invalid token.'}), 400
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        return article_createPost(id, title, body)


def articlesAdminController(request, id):
    auth_token = request.headers.get('x-access-token')
    check_id = decode_auth_token(auth_token)
    if id != check_id:
        return jsonify({'message': 'Invalid token.'}), 400
    elif request.method == 'GET':
        return articles_adminGet(id)
    elif request.method == 'DELETE':
        article_id = request.form['article_id']
        return articles_adminDelete(article_id)
