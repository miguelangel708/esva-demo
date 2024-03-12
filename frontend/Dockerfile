# Usa una imagen de Python oficial como base
FROM python:3.10.11

# Instalación de las dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    gcc \
    g++
# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8501 para Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación de Streamlit
CMD ["streamlit", "run", "chat.py"]
