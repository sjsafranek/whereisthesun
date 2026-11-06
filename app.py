from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import render_template_string

from whereisthesun import find_closest_sunny_cities


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


app = Flask(__name__, template_folder='templates', static_url_path='/static')


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/v1")
def api_v1():
    METHODS = ['FindTheSun']
    
    api_request = request.json
    
    # Check method aargument
    method = api_request.get('method')
    if not method:
        return jsonify(buildMissingParameterResponse('method')), 404
    if method not in METHODS:
        return jsonify(buildMethodNotAllowedResponse()), 405

    # Method handlers
    if 'FindTheSun' == method:

        # Required parameters
        params = api_request.get('params')
        if not params:
            return jsonify(buildMissingParameterResponse('params')), 404
        
        latitude = params.get('latitude')
        if not latitude:
            return jsonify(buildMissingParameterResponse('params.latitude')), 404
        
        longitude = params.get('longitude')
        if not longitude:
            return jsonify(buildMissingParameterResponse('params.longitude')), 404

        # Find cities
        cities = find_closest_sunny_cities(latitude, longitude, **params)

        # Format and return results
        return jsonify(buildSuccessResponse(cities=cities)), 200
