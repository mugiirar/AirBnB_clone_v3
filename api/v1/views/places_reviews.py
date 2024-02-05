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
