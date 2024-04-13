FROM python:3.11.8-slim

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /code
RUN mkdir -p /data/logs

