#!/usr/bin/python3
"""handle restful api"""


from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request

@app_views.route('/states/<state_id>/cities', methods=["GET"], strict_slashes=False)
def view_city(state_id):
    """return cities"""
    city = storage.get(State, state_id)
    if city is None:
        abort(404)
    city_list = city.cities
    list_of_cities = []
    for value in city_list:
        list_of_cities.append(value.to_dict())
    return (jsonify(list_of_cities))

@app_views.route('cities/<city_id>', methods=["GET"], strict_slashes=False)
def id_city_view(city_id):
    """ give back city with a specific id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return (jsonify(city.to_dict()))

@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def city_del(city_id):
    """delete the city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """creating a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    if 'name' not in data.keys():
        abort(400, "Missing name")

    city_obj = City(**data)
    setattr(city_obj, 'state_id', state_id)
    storage.new(city_obj)
    storage.save()
    return make_response(jsonify(city_obj.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def city_update(city_id):
    """update the city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at", "state_id"]
        if key not in ignore_keys:
            setattr(city, key, value)

    city.save()
    return (jsonify(city.to_dict()), 200)


