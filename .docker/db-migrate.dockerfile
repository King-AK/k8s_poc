# Image for db-migrate
FROM python:3.7-buster
RUN mkdir /code
WORKDIR /code
COPY ./alembic /code/alembic
COPY requirements.txt /code
RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y netcat
RUN pip install --upgrade pip && pip install wheel && pip install -r requirements.txt --quiet
