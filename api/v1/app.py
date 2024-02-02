#!/usr/bin/python3
"""api stuff"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_content(exception):
    """mathod that calls clode"""
    storage.close()

@app.errorhandler(404)
def found_not(error):
    """ 404 not found error """
    return (make_response(jsonify({'error': 'Not found'}), 404))

if __name__ == "__main__":
    # Set host and port from environment variables or use default values
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the Flask app with specified host, port, and threaded=True
    app.run(host=host, port=port, threaded=True)
