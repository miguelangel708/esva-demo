from flask import Flask,jsonify, request
from flask_cors import CORS
import GoogleDrive
import os
# import ESVA_automerging as LLM_model
from routes.auth import routes_auth
from routes.get_answer import get_answer
from routes.test_api import test_api

app = Flask(__name__)
app.register_blueprint(routes_auth, url_prefix="/api")
app.register_blueprint(get_answer, url_prefix="/api")
app.register_blueprint(test_api, url_prefix="/test")

CORS(app)

if __name__ == '__main__':
        
    app.run(debug=True, port="5000", host = "0.0.0.0")