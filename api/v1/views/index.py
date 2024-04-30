#!/usr/bin/python3
'''
Create Flask app; app_views
'''
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def api_status():
    """
    Returns a JSON response  for RESTful API health.
    """
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route('/stats')
def get_stats():
    """
    stats of all objs route
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User'),
    }

    return jsonify(stats)
