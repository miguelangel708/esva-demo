import requests
import os

def get_api_status():
    url = "https://esva-demo-soel3q6bbq-uw.a.run.app"+ "/test"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['message']
    else:
        return 'Error al obtener la respuesta de la API status'
    
def login(username, password):
    url = "https://esva-demo-soel3q6bbq-uw.a.run.app" + "/api/login"
    data = {'username': username, 'password': password }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        # Verificar si la respuesta contiene el token de portador
        bearer_token = response.text.strip()  # Eliminar espacios en blanco alrededor del token
        if bearer_token:
            return bearer_token
        else:
            return 'error'
    else:
        return 'connection error'

def validate_token(token):
    url = "https://esva-demo-soel3q6bbq-uw.a.run.app"+ "/api/verify/token"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return 'Error al obtener la respuesta de la API validate token'
    
def ask_question(query, token):
    url = "https://esva-demo-soel3q6bbq-uw.a.run.app"+ "/api/getAnswer"
    data = {'query': query}
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['message']
    else:
        return 'Error al obtener la respuesta de la API'

    

def main():
    # prueba de consultas de apis
    api_status = get_api_status()
    print(f"resultado de api_status: {api_status}")
    bearer_token = login(username="Admin@west.net.co", password="West2024")
    print(f"resultado del bearer token {bearer_token}")
    data_token = validate_token(bearer_token)
    print(f"resultado del data token {data_token}")
    response = ask_question("cuales son las causas para un despido?", bearer_token)
    print(f"respuesta a la pregunta {response}")

if __name__ == "__main__":
    main()
