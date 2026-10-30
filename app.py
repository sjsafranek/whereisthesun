"""
Simple website with an interactive map, built with Flask + Leaflet (OpenStreetMap tiles).

Setup:
    pip install flask
Run:
    python app.py
Then open http://127.0.0.1:5000
"""

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import render_template_string

from whereisthesun import find_closest_sunny_city


def buildSuccessResponse(**kwargs):
    return {
        'status': 'ok',
        'data': {
            **kwargs
        }
    }

def buildErrorResponse(message, code=500):
    return {
        'status': 'error',
        'error': {
            'code': code,
            'message': message
        }
    }

def buildMethodNotAllowedResponse():
    return buildErrorResponse('Method Not Allowed', 405)

def buildMissingParameterResponse(parameter_name):
    return buildErrorResponse( f"Missing Parameter: '{parameter_name}'", 404)


app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/v1")
def api_v1():
    METHODS = ['FindTheSun']
    
    api_request = request.json
    
    method = api_request.get('method')
    if not method:
        return jsonify(buildMissingParameterResponse('method')), 404
    if method not in METHODS:
        return jsonify(buildMethodNotAllowedResponse()), 405

    if 'FindTheSun' == method:
        params = api_request.get('params')
        if not params:
            return jsonify(buildMissingParameterResponse('params')), 404
        latitude = params.get('latitude')
        if not latitude:
            return jsonify(buildMissingParameterResponse('params.latitude')), 404
        longitude = params.get('longitude')
        if not longitude:
            return jsonify(buildMissingParameterResponse('params.longitude')), 404
        city = find_closest_sunny_city(latitude, longitude)
        return jsonify(buildSuccessResponse(city=city)), 200



if "__main__" == __name__:
    app.run(debug=True)

