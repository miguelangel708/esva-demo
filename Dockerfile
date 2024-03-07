FROM python:3.10.11

# Instalación de las dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    gcc \
    g++

# Copiar el directorio actual al contenedor en /usr/src/app
COPY . /usr/src/app

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Establecer el comando de entrada
CMD ["streamlit", "run", "ESVA_interface.py"]
