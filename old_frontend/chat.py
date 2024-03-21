import streamlit as st
import time
import requests
import os
import apiClient

bearer_token = "jk123"

class Chat:
    def __init__(self):
        self.user = None
        self.psswrd = None
        self.bearer_token = None

    def get_inputs(self):
        self.num1 = st.number_input("Ingrese el primer número:")
        self.num2 = st.number_input("Ingrese el segundo número:")

    def calculate_sum(self):
        self.result = self.num1 + self.num2

    def display_result(self):
        st.write(f"La suma de {self.num1} y {self.num2} es: {self.result}")
        

def insert_newlines(text, every=75):
    return '\n'.join(text[i:i+every] for i in range(0, len(text), every))

def on_button_click(username, password):
    global bearer_token
    # bearer_token = apiClient.login(username="Admin@west.net.co", password="West2024")
    bearer_token = apiClient.login(username, password)
    if(bearer_token == 'error'): 
        st.sidebar.write("no se pudo conectar con la api")
        return
    if(bearer_token == 'connection error'): 
        st.sidebar.write("credenciales invalidas")
        return
    st.sidebar.write(f"resultado del bearer token {bearer_token}")
    
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
    
    st.sidebar.title("Modulo de inicio de sesión:"  )
    
    # st.sidebar.subheader("Usuario")
    user_input = st.sidebar.text_input("User")
    
    # st.sidebar.subheader("Contraseña")
    password_input = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Validar"):  on_button_click(user_input, password_input)
    
    st.sidebar_state = False


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
            
            # if ( query == "test"):
            #     response  =  get_answer()
            # else:
            #     response  =  post_answer(query)
            response = "debes iniciar sesión"
            print(f"token recibido {bearer_token}")
            if (bearer_token != 'jk123'):
                response = apiClient.ask_question(bearer_token, query)
            
            # response = f"respuesta a la pregunta {query}"
            response = insert_newlines(response,76)
            # response  = responseTest.response(query)
            thinking_message.text(response)

        # save the answer on messages to load the history in line 26
        st.session_state.messages.append({"role":"assistant","content":response})


if __name__ == '__main__':
    main()