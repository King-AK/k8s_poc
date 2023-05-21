# Image for the Harvester
FROM python:3.7-buster
RUN mkdir /code
WORKDIR /code
COPY ./Ingestor /code/Ingestor
COPY requirements.txt /code
COPY ingestor.py /code/ingestor.py
RUN pip install --upgrade pip && pip install wheel && pip install -r requirements.txt --quiet