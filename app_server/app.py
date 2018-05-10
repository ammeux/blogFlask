import os

from flask import (Flask, request)

from Controllers.articlesController import (articlesController, articleCreateController, articlesAdminController)

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
        return "Welcome to my Blog"

    @app.route('/articles/<int:id>/show', methods=['GET'])
    def articles_show(id):
        return articlesController(request, id)

    @app.route('/articles/<int:id>/create', methods=['POST'])
    def article_create(id):
        return articleCreateController(request, id)

    @app.route('/articles/<int:id>/admin', methods=('GET', 'DELETE'))
    def articles_admin(id):
        return articlesAdminController(request, id)

    from Config import db
    db.init_app(app)

    import auth
    app.register_blueprint(auth.bp)

    return app
