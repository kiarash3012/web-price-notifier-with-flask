from flask import Blueprint
from flask import request
from flask import session
from flask import url_for
from flask import render_template
from werkzeug.utils import redirect
from src.models.users.user import User
import src.models.users.errors as UserErrors


user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if(request.method==['POST']):
        email = request.form['email']
        password = request.form['hashed']
        print(email)
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/login.html')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if (request.method == ['POST']):
        email = request.form['email']
        password = request.form['hashed']
        print(email)
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')


@user_blueprint.route('/alerts')
def user_alerts():
    return 'this is the alert page.'


@user_blueprint.route('/logout')
def logout_user():
    pass


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass


