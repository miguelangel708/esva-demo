import streamlit as st
import time
import openai
import os
from llama_index.llms import OpenAI
from llama_index import (
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index import StorageContext, load_index_from_storage
from llama_index.retrievers import AutoMergingRetriever
from llama_index.indices.postprocessor import SentenceTransformerRerank
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.embeddings import HuggingFaceEmbedding
from openai import AuthenticationError


openai.api_key = None
query_engine = None

# # OpenAI API key
def printOpenAiKey(key):
    global query_engine
    openai.api_key = key
    print(f"this is the openai api key {openai.api_key}")
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    index = load_automerging_index(
        llm=llm,
        save_dir='./files/ft_merging_index',  #merging means that the docs are separated
    )
    query_engine = get_automerging_query_engine(index, similarity_top_k=6)
    
# Load LLM

# load vector index database
def load_automerging_index(
    llm,
    embed_model="sentence-transformers/all-MiniLM-L6-v2",
    save_dir="merging_index",
):
    if not os.path.exists(save_dir):
        print("no se encontró base de datos")
    else:
        merging_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=HuggingFaceEmbedding(model_name=embed_model),
    )
        automerging_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=merging_context,
        )
    return automerging_index

# load the model 
def get_automerging_query_engine(
    automerging_index,
    similarity_top_k=12,
    rerank_top_n=6,
):
    base_retriever = automerging_index.as_retriever(similarity_top_k=similarity_top_k)
    retriever = AutoMergingRetriever(
        base_retriever, automerging_index.storage_context, verbose=True
    )
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )
    auto_merging_engine = RetrieverQueryEngine.from_args(
        retriever, node_postprocessors=[rerank]
    )
    return auto_merging_engine

def process_answer(query):
    try:
        if openai.api_key == None: return "ingrese la open ai key"
        
        response = query_engine.query(query)
        source_documents = response.source_nodes[0].metadata['file_name']
        page_list = [int(i.metadata['page_label']) for i in response.source_nodes]
        #page_list = sorted(list(set(page_list)))
        #page_list = ', '.join(map(str, set(page_list)))
        page_list.sort()
        if(source_documents =="Instructivo_Diligenciamiento_Formato_Reporte_de_Eficiencia_de_Combustion_en_T_1PDJHb8.pdf"):
            source_documents = "Instructivo_Diligenciamiento_1PDJHb8"
        pass
    except AuthenticationError as e:
        print(e)
        return "llave open ai invalida"
    
    return response.response + f' \n Documento Fuente: {source_documents} \n Paginas: {page_list}'

def init():
    
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
    
    #barra lateral para ingresar la llave de openai 
    left_column = st.sidebar
    with left_column:
        text = st.empty()
        key = text.text_input("Ingrese la llave de open ai", value="", key="1")
        boton = st.button("Enviar")

        if boton and key:
            printOpenAiKey(key)
            text.text_input("Ingrese la llave de open ai", value="", key="2")   
        
    # user query
    query = st.chat_input("enter your question")

    if query:

        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.messages.append({"role":"user","content":query})

        with st.chat_message("assistant"):
            thinking_message = st.empty()  # Empty container for message "thinking..."
            time.sleep(0.5)
            thinking_message.text("thinking...")  # We use st.text instead of st.markdown
            # here in the response put the result of the RAG model
            response  = process_answer(query)
            # response  = "respuesta sin IA"
            thinking_message.text(response)

        # save the answer on messages to load the history in line 26
        st.session_state.messages.append({"role":"assistant","content":response})


def main():
    init()

if __name__ == '__main__':
    main()