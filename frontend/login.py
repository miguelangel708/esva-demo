# login.py
import streamlit as st
import json

# Cargar los datos de los usuarios desde el archivo JSON
with open('./files/usuarios.json') as f:
    data = json.load(f)
    usuarios = data['usuarios']

def autenticar(username, password):
    for usuario in usuarios:
        if usuario['username'] == username and usuario['password'] == password:
            return True
    return False

def main():
    st.markdown(
        """
        <div style='text-align:center;'>
            <h1>Inicio de Sesión ESVA</h1>
            <p>Bienvenido al ESVA, tu asistente virtual, por favor inicia sesión para acceder</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 3, 1])  # Dividir el espacio en tres columnas, la columna central será la más ancha

    with col2:  # Utilizar la columna central para centrar los elementos horizontalmente
        # Input de usuario y contraseña
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Iniciar Sesión"):
            if autenticar(username, password):
                st.session_state.logged_in = True  # Establecer la bandera de sesión
                st.rerun()  # Reiniciar la aplicación para redirigir al usuario
            else:
                st.error("Credenciales incorrectas")
    

if __name__ == "__main__":
    main()
