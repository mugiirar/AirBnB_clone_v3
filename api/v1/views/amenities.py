#!/usr/bin/python3
"""handle api requests"""
from flask import jsonify, make_response, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views

@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def view_amenities():
    """amenity list"""
    list_amenities = []
    for value in storage.all(Amenity).values():
        list_amenities.append(value.to_dict())

    return (jsonify(list_amenities))

@app_views.route('/amenities/<amenity_id>', methods=["GET"], strict_slashes=False)
def view_amenity:
    """gets amenities"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return (jsonify(amenity.to_dict()))

@app_views.route('/amenities/<amenity_id>', methods=["DELETE"], strict_slashes=False)
def amenity_delete(amenity_id):
    """delete amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)

@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """new amenity"""
    data = request.get_json()
    if not data:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if 'name' not in data.keys():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    new_amen = Amenity(**data)
    new_amen.save()
    return (jsonify(new_amen.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=["PUT"], strict_slashes=False)
def amenity_update(amenity_id):
    """updating amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(amenity, key, value)

    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
