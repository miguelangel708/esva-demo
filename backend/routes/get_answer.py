from flask import Blueprint, request
from flask import jsonify
from function_jwt import validate_token
from ESVA_automerging import process_answer


get_answer = Blueprint("get_answer", __name__)

@get_answer.before_request
def verify_token_middleware():
    # cuando la consulta se hace via fetch, se envia una request de validación 
    # que espera un mensaje 200 para hacer la request real, dado que el middleware
    # esta en before request, por aquí pasa primero la validación, por lo que se debe responder
    # un mensaje de 200 si el metodo es alguno de options
    if request.method == 'OPTIONS':
        return '', 200
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]
        return validate_token(token, output=False)
    else:
        return jsonify({"message": "Missing Authorization header"}), 401
    
    
@get_answer.route("/getAnswer", methods= ["POST", "OPTIONS"])
def gestAnswer():
    data = request.get_json()
    query = data['query']
    response = process_answer(query)
    print(response)
    return jsonify({"message":f"respuesta desde la api, {response}"}),200