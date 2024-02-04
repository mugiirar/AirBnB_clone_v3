#!/usr/bin/python3
"""handle places api"""

from models.city import City
from models.user import User
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request

@app_views.route('/cities/<city_id>/places', methods=["GET"], strict_slashes=False)
def give_place(city_id):
    """give back the city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([obj.to_dict() for obj in city.places])

@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def place_finder(place_id):
    """give a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return (jsonify(place.to_dict()))

@app_views.route('/cities/<city_id>/places', methods=["POST"], strict_slashes=False)
def post_place(city_id):
    """posting a new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if 'user_id' not in data.keys():
        abort(404, 'Missing user_id')

    user = storage.get(User, data["user_id"])

    if user is None:
        abort(404)

    if 'name' not in data.keys():
        abort(400, 'Missing name')

    new_obj=Place(**data)
    setattr(new_obj, 'city_id', city_id)
    storage.new(new_obj)
    storage.save()
    return (jsonify(new_obj.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Delete place object"""
    place_to_delete = storage.get(Place, place_id)
    if place_to_delete is None:
        abort(404)
    storage.delete(place_to_delete)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def places_mod(place_id):
    """modify a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at", "city_id", "user_id"]
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return (jsonify(place.to_dict()), 200)
