from flask import Blueprint, request
from flask import jsonify
from function_jwt import validate_token
from ESVA_automerging import process_answer

get_answer = Blueprint("get_answer", __name__)

@get_answer.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    # the return is necessary to validate the token,
    # if you remove only the return the getAnswer function
    # would work without validation
    return validate_token(token, output=False)

@get_answer.route("/getAnswer", methods= ["POST"])
def gestAnswer():
    data = request.get_json()
    query = data['query']
    response = process_answer(query)
    return jsonify({"message":f"respuesta desde la api, {response}"})