from flask import Blueprint, request
from function_jwt import write_token, validate_token
from flask import jsonify

routes_auth = Blueprint("routes_auth", __name__)

def validateUser(user, password):
    validate= False
    if user == "Admin@west.net.co" and password == "West2024":
        validate = True
    return validate

@routes_auth.route("/login", methods = ["POST"])
def login():

    data = request.get_json()
    user = data["username"]
    password =data["password"]

    if  validateUser(user, password):
        response = write_token(data=request.get_json())
    else:
        response = jsonify({"message":"user not found"})
        response.status_code = 404
    
    return response
    
@routes_auth.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output = True)