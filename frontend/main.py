# main.py
import streamlit as st
from login import main as login_main
from chat import main as main_page_main

# Configuración de la página
st.set_page_config(
            page_title="ESVA",
            page_icon="https://west.net.co/wp-content/uploads/2023/06/Logo-Usuario-jpg.jpg"
        )

# Verificar si el usuario ha iniciado sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main_page_main()  # Mostrar la página principal
else:
    login_main()  # Mostrar la página de login
