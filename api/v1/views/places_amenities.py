#!/usr/bin/python3
""" handle link """
from models.place import Place
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request

@app_views.route('/places/<place_id>/amenities', methods=["GET"], strict_slashes=False)
def amenity_view(place_id):
    """retrieves all amenities"""
    get_id = storage.get(Place, place_id)
    if get_id is None:
        abort(404)
    amenity_dict = get_id.amenities
    amenity_list = []
    for value in amenity_dict:
        amenity_list.append(value.to_dict())
    return (jsonify(amenity_list))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE"], strict_slashes=False)
def places_delete(place_id, amenity_id):
    """ delete amenity obj by amenity_id """
    amen_id = storage.get(Amenity, amenity_id)
    if amen_id is None:
        abort(404)
    plac_id = storage.get(Place, place_id)
    if plac_id is None:
        abort(404)
    amenities_object = plac_id.amenities
    if amen_id not in amenities_object:
        abort(404)
    for item in amenities_object:
        if item.id == amenity_id:
            amenities_object.remove(item)
            storage.save()
            return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=["POST"],
                 strict_slashes=False)
def create_amenity_link(place_id, amenity_id):
    """ creating a amenity link to a place """
    plac_id = storage.get(Place, place_id)
    if plac_id is None:
        abort(404)
    amen_id = storage.get(Amenity, amenity_id)
    if amen_id is None:
        abort(404)
    amenities_object = plac_id.amenities
    for item in amenities_object:
        if item.id == amenity_id:
            return (jsonify(amen_id.to_dict()), 200)
        else:
            amenities_object.append(amen_id)
            storage.save()
            return (jsonify(amen_id.to_dict()), 201)
