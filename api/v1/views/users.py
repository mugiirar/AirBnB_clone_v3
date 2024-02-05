#!/usr/bin/python3
"""handle api"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.user import User


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def get_users():
    """give back users"""
    users = storage.all(User).values()
    list_users = []

    for user in users:
        list_users.append(user.to_dict())

    return (jsonify(list_users))


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def specif_user(user_id):
    """give specific user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return (jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=["DELETE"], strict_slashes=False)
def del_user(user_id):
    """delete a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """create a new user"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'email' not in data.keys():
        return (make_response(jsonify({'error': 'Missing email'}), 400))
    if "password" not in data.keys():
        return (make_response(jsonify({'error': 'Missing password'}), 400))
    new_user = User(**data)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def modify_user(user_id):
    """mod user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(user, key, value)

    user.save()
    return (jsonify(user.to_dict()), 200)
