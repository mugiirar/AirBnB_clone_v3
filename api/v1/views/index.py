#!/usr/bin/python3
"""indexing"""

from api.v1.views import app_views
from flask import jsonify
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City


@app_views.route('/status')
def status():
    """ returns a JSON"""
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    """number of each object by type """
    counter = {"amenities": storage.count(Amenity),
               "cities": storage.count(City),
               "places": storage.count(Place),
               "reviews": storage.count(Review),
               "states": storage.count(State),
               "users": storage.count(User)}
    return (jsonify(counter))
