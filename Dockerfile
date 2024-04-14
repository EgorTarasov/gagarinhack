FROM python:3.11.5-bullseye

WORKDIR /code

COPY requirements/base.txt requirements/base.txt
COPY requirements/prod.txt requirements/prod.txt
RUN pip3 install -r requirements/prod.txt
COPY . /code
RUN mkdir -p /data/logs