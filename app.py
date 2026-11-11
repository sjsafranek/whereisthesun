import re
import time
import logging
from logging.config import dictConfig

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import render_template_string
# from werkzeug import serving
from flask import g

from api_v1 import v1
import api_helpers



app = Flask(__name__, template_folder='templates', static_url_path='/static')
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

###########
# LOGGING #
###########

# Configure logging BEFORE creating the Flask app instance
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            # 'format': '%(asctime)s [%(levelname)s] [%(threadName)s] %(filename)s %(funcName)s:%(lineno)d %(message)s',
            'format': '%(asctime)s [%(levelname)s] [%(process)d] %(filename)s %(funcName)s:%(lineno)d %(message)s',
        }
    },
    'handlers': {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        },
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
        # 'file': {
        #     'class': 'logging.FileHandler',
        #     'filename': 'app.log',
        #     'formatter': 'default'
        # }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})

# Mute the Werkzeug request logger
logging.getLogger('werkzeug').disabled = True



@app.before_request
def before_request():
    # Store the start time in Flask's global 'g' object per request
    g.start_time = time.time()
    app.logger.info(f"IN  {request.remote_addr} {request.method} {request.path} - {request.content_length or 0}B")

@app.after_request
def after_request(response):
    # Calculate total duration of the request
    duration = time.time() - g.start_time
    
    # Log HTTP method, URL path, response status, and duration
    app.logger.info(f"OUT {request.remote_addr} {request.method} {request.path} [{response.status_code}] {duration:.4f}s - {response.content_length}B")
    return response


# Add API endpoints
app.register_blueprint(v1, url_prefix='/api/v1')

# Add views
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

