import streamlit as st
import time
import sys
import os

# codigo para importar el backend como script y hacer el llamado
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_path)
import ESVA_automerging as LLM_model

def insert_newlines(text, every=76):
    """
    Inserta un salto de línea cada 'every' caracteres en el texto dado.
    """
    return '\n'.join(text[i:i+every] for i in range(0, len(text), every))


def main():
    
    # page content
    st.set_page_config(
        page_title="ESVA",
        page_icon="https://west.net.co/wp-content/uploads/2023/06/Logo-Usuario-jpg.jpg"
    )

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
            response  = LLM_model.process_answer(query)
            response = insert_newlines(response)
            # response  = "respuesta sin IA"
            thinking_message.text(response)

        # save the answer on messages to load the history in line 26
        st.session_state.messages.append({"role":"assistant","content":response})


if __name__ == '__main__':
    main()