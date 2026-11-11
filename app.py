from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import render_template_string

import api_v1 as v1
import api_helpers


app = Flask(__name__, template_folder='templates', static_url_path='/static')

# app.register_blueprint(v1, url_prefix='/api/v1')


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/v1")
def api_v1(): 
    api_request = request.json
    
    # Check method aargument
    method = api_request.get('method')
    if not method:
        return jsonify(api_helpers.buildMissingParameterResponse('method')), 404

    # Method handlers
    if 'FindTheSun' == method:
        return v1.findTheSun(api_request)
    
    # Handle method not allowed
    return jsonify(api_helpers.buildMethodNotAllowedResponse()), 405

