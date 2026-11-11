from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import render_template_string

from api_v1 import v1
import api_helpers


app = Flask(__name__, template_folder='templates', static_url_path='/static')
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# Add API endpoints
app.register_blueprint(v1, url_prefix='/api/v1')

# Add views
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

