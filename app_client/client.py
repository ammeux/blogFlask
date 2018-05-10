import os

from flask import (Flask, render_template, request)

from Controllers.usersController import (userAdminGet, userLoginForm, userLoginPost, userRegisterForm, userRegisterMake, userAdminPut, userAdminDelete, userLogout)
from Controllers.articlesController import (articlesGet, articleCreateGet, articleCreatePost, articlesAdminGet, articlesAdminDelete)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(dict(
        DATABASE=os.path.join(app.root_path, 'user.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default'
    ))

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/<int:id>/userAdmin', methods=('GET', 'POST'))
    def userAdmin(id):
        if request.method == 'GET':
            return userAdminGet(id, request)
        elif request.method == 'POST':
            if request.form['submit'] == 'Modify':
                return userAdminPut(id, request)
            if request.form['submit'] == 'Delete':
                return userAdminDelete(id, request)

    @app.route('/<int:id>/articles', methods=['GET'])
    def articles(id):
        return articlesGet(id, request)

    @app.route('/<int:id>/articleCreate', methods=('GET', 'POST'))
    def articleCreate(id):
        if request.method == 'GET':
            return articleCreateGet(id)
        elif request.method == 'POST':
            return articleCreatePost(id, request)

    @app.route('/<int:id>/articlesAdmin', methods=('GET', 'POST'))
    def articlesAdmin(id):
        if request.method == 'GET':
            return articlesAdminGet(id, request)
        elif request.method == 'POST':
            return articlesAdminDelete(id, request)

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'GET':
            return userLoginForm()
        if request.method == 'POST':
            return userLoginPost(request)

    @app.route('/register', methods=('GET', 'POST'))
    def register():
        if request.method == 'GET':
            return userRegisterForm()
        if request.method == 'POST':
            return userRegisterMake(request)

    @app.route('/logout', methods=['GET'])
    def logout():
        return userLogout()

    return app
