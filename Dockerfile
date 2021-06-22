FROM python:3.9-alpine

MAINTAINER Arnab Das arnabdas.619@gmail.com

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app


RUN adduser -D user
USER user

