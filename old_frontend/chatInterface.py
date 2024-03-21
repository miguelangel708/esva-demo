import streamlit as st
import time
import apiClient
import os 

class Chat:
    
    def __init__(self):
        self.user = None
        self.psswrd = None
        self.bearer_token = None
        self.query = None
        
    def print_bearer_token(self):
        st.sidebar.write(f"resultado del bearer token {self.bearer_token}")

    
    def insert_newlines(self, text, every=75):
        return '\n'.join(text[i:i+every] for i in range(0, len(text), every))

    
    def on_button_click(self, username, password):
        bearer_token = apiClient.login(username, password)
        if(bearer_token == 'error'): 
            st.sidebar.write("no se pudo conectar con la api")
            return
        if(bearer_token == 'connection error'): 
            st.sidebar.write("credenciales invalidas")
            return
        self.bearer_token = bearer_token
        os.environ["TOKEN"] = bearer_token 
        st.sidebar.write(f"resultado del bearer token {self.bearer_token}")

        #el bearer token deja se ser None después de pasar por las validaciones
        # por lo que revisar que sea None es una forma de validar que se haya iniciado sesión 
        
        
    def query_ask_api(self):
        try:
            if(self.bearer_token == None):
                return "inicie sesión"
            response = apiClient.ask_question(self.bearer_token, self.query)
            response = self.insert_newlines(response,76)
        except Exception as e:
            response = f"error al hacer la consulta con la api {e}"
        return response
        
    
    def load_tittle_logo(self):
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


    def load_login(self):
        st.sidebar.title("Modulo de inicio de sesión:"  )
    
        user_input = st.sidebar.text_input("User")
        password_input = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Validar"):  self.on_button_click(user_input, password_input)
    
    
    def load_chat(self):    
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
            
        query = st.chat_input("enter your question")

        if query:
            self.query = query
            with st.chat_message("user"):
                st.markdown(query)
            st.session_state.messages.append({"role":"user","content":query})

            with st.chat_message("assistant"):
                thinking_message = st.empty()  # Empty container for message "thinking..."
                time.sleep(0.5)
                thinking_message.text("pensando...")  # We use st.text instead of st.markdown
                response = apiClient.ask_question(query, os.getenv('TOKEN'))
                # response = f"token recibido en chat {os.getenv('TOKEN')}"
                response = self.insert_newlines(response)
                thinking_message.text(response)

            st.session_state.messages.append({"role":"assistant","content":response})


       
def main():
    
    chat = Chat()
    
    chat.load_tittle_logo()
    
    chat.load_login()
    
    if (os.getenv("TOKEN") != None):
        chat.load_chat()



if __name__ == '__main__':
    main()