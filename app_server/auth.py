from Controllers.usersController import (registerController, loginController, userAdminController)

from flask import (Blueprint, request)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    return registerController(request)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    return loginController(request)


@bp.route('/<int:id>/update', methods=('PUT', 'DELETE', 'GET'))
def update(id):
    return userAdminController(request, id)
