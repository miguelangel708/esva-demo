from flask import Flask,jsonify, request
from flask_cors import CORS
import GoogleDrive
import os
import ESVA_automerging as LLM_model


app = Flask(__name__)
CORS(app)

def process_question(question):
    GoogleDrive.login()
    # ruta_relativa = './files'
    carpeta = './files'
    ruta_absoluta = os.path.abspath('./files') + '/'
    GoogleDrive.bajar_archivo_por_id('1zRpE_C7rDWdvAynNk1D9C2WrDlHlYS4p',ruta_absoluta)
    GoogleDrive.bajar_archivo_por_id('1vKXwTgrfjYq9UCsFxx6mZtgnXW0CpF2R',ruta_absoluta)
    GoogleDrive.bajar_archivo_por_id('1VNvu9-JvO1Z2dz6fXetsjCEzKudq3nrr',ruta_absoluta)
    GoogleDrive.bajar_archivo_por_id('1NJl98Yo4Lb4N2xLPvbmdG2r2gNRzjHM0',ruta_absoluta)
    GoogleDrive.bajar_archivo_por_id('1v0uP6l5S2QBVTAE2b40o-U1kVx9fwYaq',ruta_absoluta)
    if os.path.exists(carpeta) and os.path.isdir(carpeta):
        # Obtener la lista de archivos en la carpeta
        archivos = os.listdir(carpeta)
        # Imprimir los nombres de los archivos
        info_archivos = "Archivos en la carpeta 'files':\n"
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta, archivo)
            tamaño = os.path.getsize(ruta_completa)
            info_archivos += f"Archivo: {archivo} - Tamaño: {tamaño} bytes\n"
            print(info_archivos)
    else:
        print("no se encontraron archivos")
        
    return "Esta es una respuesta a tu pregunta: " + question + " info " + info_archivos



@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'API home fucnionando!'})



@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'API test funcionando correctamente!'})


@app.route('/getFilesInfo', methods=['POST'])
def askQuestion():
    data = request.get_json()
    question = data['question']
    response = process_question(question)
    return jsonify({'response': response})


@app.route('/askQuestion', methods=['POST'])
def getMyInfo():
    data = request.get_json()
    if 'question' in data:
        pregunta = data['question']
        respuesta = LLM_model.process_answer(pregunta)
        response_message = "respuesta desde la api: '{}'".format(respuesta)
    else:
        response_message = "Por favor, proporciona una pregunta en el cuerpo de la solicitud."
    value = {
        "response": response_message
    }
    return jsonify(value)


if __name__ == '__main__':
    app.run(port=5000)