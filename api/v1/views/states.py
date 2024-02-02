#!/usr/bin/python3
"""handle api"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_view():
    """ return a jsonified states objects """
    objs = storage.all(State)
    return jsonify([obj.to_dict() for obj in objs.values()])

@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def states_id_view(state_id):
    """ state obj by state_id """
    getter_id = storage.get(State, state_id)
    if getter_id is None:
        abort(404)
    return (jsonify(getter_id.to_dict()))

@app_views.route('/states/<state_id>', methods=["DELETE"], strict_slashes=False)
def delete_id_state(state_id):
    """delete the city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}), 200)

@app_views.route('states', methods=["POST"], strict_slashes=False)
def state_maker():
    """create a new state"""
    n_state = request.get_json()
    if not n_state:
        abort(400, "Not a JSON")
    if 'name' not in n_state.keys():
        abort(400, "Missing name")
    new_state = State(**n_state)
    storage.new(new_state)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def state_update(state_id):
    """state object update"""
    the_id = storage.get(State, state_id)
    if the_id is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(the_id, key, value)
    the_id.save()
    return (jsonify(the_id.to_dict()), 200)

