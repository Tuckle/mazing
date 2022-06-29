from flask import Blueprint, request
from flask import jsonify, Response
from api.models import User, db
from api.core import create_response
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                unset_jwt_cookies, get_jwt)
from werkzeug.security import generate_password_hash, check_password_hash

blueprint = Blueprint("user", __name__)


@blueprint.route('/user', methods=("POST",))
def create_user():
    data = request.get_json()

    try:
        assert data.get("username"), "No username provided for user."
        assert data.get("password"), "No password provided for user."
    except AssertionError as aer:
        return create_response(status=422, message=str(aer))
    defaults = {x: data[x] for x in ["username", "password"] if data.get(x)}
    defaults["password"] = generate_password_hash(defaults["password"])

    user, created = User.get_or_create(User, defaults, username=data["username"])
    if not created:
        return create_response(status=409, message=f"User already exists.")

    return create_response(message="User created.")


@blueprint.route('/login', methods=("POST",))
def login_user():
    data = request.get_json()

    try:
        assert data.get("username"), "No username provided for user."
        assert data.get("password"), "No password provided for user."
    except AssertionError as aer:
        return create_response(status=422, message=str(aer))

    user = db.session.query(User).filter_by(username=data["username"]).first()
    if not user:
        return create_response(status=404, message="User does not exist.")

    if not check_password_hash(user.password, data["password"]):
        return create_response(status=401, message=f"Invalid credentials for {data['username']}")

    access_token = create_access_token(identity=str(user.id))
    # refresh_token = create_refresh_token(identity=data['username'])

    return create_response(data={
        'username': data['username'],
        'access_token': access_token,
        # 'refresh_token': refresh_token
    })


@blueprint.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return create_response(message="logout successful")
