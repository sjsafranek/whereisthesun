from flask import jsonify
from flask import request
from flask import Blueprint
from flask import current_app

import api_helpers
from whereisthesun import find_closest_sunny_cities


v1 = Blueprint('v1', __name__)


@v1.route('/sun', methods=['POST'])
def find_the_sun():
    api_request = request.json

    # Required parameters
    params = api_request.get('params')
    if not params:
        return jsonify(api_helpers.buildMissingParameterResponse('params')), 404
    
    latitude = params.get('latitude')
    if not latitude:
        return jsonify(api_helpers.buildMissingParameterResponse('params.latitude')), 404
    
    longitude = params.get('longitude')
    if not longitude:
        return jsonify(api_helpers.buildMissingParameterResponse('params.longitude')), 404

    # Find cities
    current_app.logger.info(params)
    cities = find_closest_sunny_cities(latitude, longitude, **params)

    # Format and return results
    return jsonify(api_helpers.buildSuccessResponse(cities=cities)), 200

