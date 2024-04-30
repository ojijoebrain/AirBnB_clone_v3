#!/usr/bin/python3
"""
Create users etc...
"""
from flask import jsonify, abort, request, user
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_all_users():
    """
    Retrieves the user objects.
    """
    user = storage.all(User).values()
    return jsonify([user.to_dict() for user in user])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_users(user_id):
    """
    Retrieves the user objects.
    """
    users = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route('/users/<user_id>', method=["DELETE"],
                 strict_slashes=False)
def delete_users(user_id):
    """
    Retrieves the user objects.
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return  jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/users/<user_id>', method=["POS"],
                 strict_slashes=False)
def create_users(user_id):
    """
    Retrieves the user objects.
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
    return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        return abort(400, 'Missing name')
    if 'password' not in data:
        return abort(400, 'Missing password')

    user = user(**data)
    user.save()

    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', method=['PUT'],
                 strict_slashes=False)
def update_users(user_id):
    """
    update the user objects.
    """
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            return abort(404, 'Not a JSON')
        if request.content_type != 'application/json':
            return abort(404, 'Not a JSON')
        data = request.get_json()

        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        return abort(400)
