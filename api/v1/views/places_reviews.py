#!/usr/bin/python3
"""place review api"""

from models.review import Review
from models.user import User
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request

@app_views.route('/places/<place_id>/reviews', methods=["GET"], strict_slashes=False)
def review_view(place_id):
    """get revies for a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews = storage.all(Reviews)

    review_list  = []
    for review in reviews.values():
        if review.place_id == place_id:
            review_list.append(review.to_dict())

    return (jsonify(review_list))

@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def reviews_id_view(review_id):
    """get a specific review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return(jsonify(review.to_dict()))

@app_views.route('/reviews/<review_id>', methods=["DELETE"], strict_slashes=False)
def review_del(review_id):
    """delete a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return (jsonify({}), 200)

@app_views.route('/places/<place_id>/reviews', methods=["POST"], strict_slashes=False)
def new_review(place_id):
    """create a review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")

    user = storage.get(User, data["user_id"])

    if user is None:
        abort(404)

    if "text" not in data.keys():
        abort(400, "Missing text")

    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)

@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def update_mod(review_id):
    """mod review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at", "place_id", "user_id"]
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return (jsonify(review.to_dict()), 200)
