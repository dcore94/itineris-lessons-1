FROM python:3.10.15-slim-bullseye

RUN apt-get update && apt-get install -y git curl unzip jq

RUN mkdir methods
WORKDIR /methods

COPY requirements.txt /methods/
RUN pip install -r requirements.txt 

COPY download-from-ws.sh upload-to-ws.sh /methods/
RUN chmod 755 *.sh