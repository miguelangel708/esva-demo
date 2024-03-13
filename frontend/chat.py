import streamlit as st
import time
import requests
import os

# POST
def post_answer(question):
    url = os.environ['Backend-Path'] + '/askQuestion'
    data = {'question': question}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return 'Error al obtener la respuesta de la API'

# GET   
def get_answer():
    url = os.environ['Backend-Path'] + '/test'  
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['message']
    else:
        return 'Error al obtener la respuesta de la API'

def insert_newlines(text, every=75):
    """
    Inserta un salto de línea cada 'every' caracteres en el texto dado.
    """
    return '\n'.join(text[i:i+every] for i in range(0, len(text), every))


def main():

    # Page title and logo
    url_image = "https://west.net.co/wp-content/uploads/2024/01/westlogo.png"

    image_html = f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <img src="{url_image}" style="max-width: 200px; max-height: 200px;">
        </div>
    """
    page_title = "<h1 style='text-align: center;'>ESVA Document AI Chat</h1>"

    st.markdown(image_html, unsafe_allow_html=True)
    st.markdown(page_title, unsafe_allow_html=True)

    # initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    # user query
    query = st.chat_input("enter your question")

    if query:

        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.messages.append({"role":"user","content":query})

        with st.chat_message("assistant"):
            thinking_message = st.empty()  # Empty container for message "thinking..."
            time.sleep(0.5)
            thinking_message.text("pensando...")  # We use st.text instead of st.markdown
            # here in the response put the result of the RAG model
            
            if ( response == "test"):
                response  =  get_answer(query)
            else:
                response  =  post_answer(query)
                
            response = insert_newlines(response,76)
            # response  = responseTest.response(query)
            thinking_message.text(response)

        # save the answer on messages to load the history in line 26
        st.session_state.messages.append({"role":"assistant","content":response})


if __name__ == '__main__':
    main()