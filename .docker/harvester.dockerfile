# Image for the Harvester
FROM python:3.7-buster
RUN mkdir /code
WORKDIR /code
COPY ./Harvester /code/Harvester
COPY requirements.txt /code
COPY harvester.py /code/harvester.py
RUN pip install --upgrade pip && pip install wheel && pip install -r requirements.txt --quiet