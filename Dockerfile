FROM python:3.10.11-alpine

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN apk update && \
    apk add --no-cache \
    python3-dev \
    build-base \
    gcc \
    g++

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT streamlit run ESVA_interface.py
