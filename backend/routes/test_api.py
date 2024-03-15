from flask import Blueprint, request
from flask import jsonify
test_api = Blueprint("test_api", __name__)

# @test_api.before_request
# def verify_token_middleware():
#     token = request.headers['Authorization'].split(" ")[1]
#     validate_token(token, output=False)

@test_api.route("/", methods= ["GET"])
def gestAnswer():
    return jsonify({"message":f"API funcionando correctamente"})