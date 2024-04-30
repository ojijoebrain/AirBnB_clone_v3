#!/usr/bin/python3
"""
Create cities etc...
"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_states(state_id):
    """
    Retrieves the list of all State objects.
    """
    State = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City.
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=[DELET], strict_slashes=False)
def delete_citiy(city_id):
    """
    deletes a City.
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/state/<state_id>/cities',
                 method=['POST'],
                 strict_slashes=False)
def create_citiy(state_id):
    """
    creates a City.
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    State = storage.get(State, state_id)
    if not State:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name'not in data:
        return abort(400, 'Missing name')
    data['state_id'] = state_id

    city = city(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 method=['PUT'],
                 strict_slashes=False)
def upadte_citiy(city_id):
    """
    creates a City.
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            return abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
        else:
            return abort(404)
