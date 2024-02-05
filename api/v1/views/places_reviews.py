#!/usr/bin/python3
""" Handles all default RestFul API actions """

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.review import Review
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """ Return a jsonified review objects by place_id """
    place_instance = storage.get(Place, place_id)
    if place_instance is None:
        abort(404)
    
    review_dict = storage.all(Review)
    review_list = [value.to_dict() for value in review_dict.values() if value.place_id == place_id]
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def get_review_by_id(review_id):
    """ Returns a jsonified review object by review_id """
    review_instance = storage.get(Review, review_id)
    if review_instance is None:
        abort(404)
    
    return jsonify(review_instance.to_dict())


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete review object by review_id """
    review_instance = storage.get(Review, review_id)
    if review_instance is None:
        abort(404)
    
    storage.delete(review_instance)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ Creating a review object """
    place_instance = storage.get(Place, place_id)
    if place_instance is None:
        abort(404)
    
    data_request = request.get_json()
    if not data_request:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    if "user_id" not in data_request:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    
    user_instance = storage.get(User, data_request["user_id"])
    if user_instance is None:
        abort(404)
    
    if "text" not in data_request:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    
    data_request["place_id"] = place_id
    new_review_obj = Review(**data_request)
    new_review_obj.save()
    return jsonify(new_review_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ Updating a review object """
    review_instance = storage.get(Review, review_id)
    if review_instance is None:
        abort(404)
    
    data_request = request.get_json()
    if not data_request:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    ignore_keys = ["id", "created_at", "updated_at", "place_id", "user_id"]
    for key, value in data_request.items():
        if key not in ignore_keys:
            setattr(review_instance, key, value)
    
    review_instance.save()
    return jsonify(review_instance.to_dict()), 200

