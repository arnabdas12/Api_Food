FROM python:3.9-alpine

MAINTAINER Arnab Das arnabdas.619@gmail.com

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt
Run apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app


RUN adduser -D user
USER user

