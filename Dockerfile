# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
ARG POLIGON_API
ARG LUNCHMONEY_API

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY stock_updater.py stock_updater.py
COPY config.yaml config.yaml

RUN python3 stock_updater.py $POLIGON_API $LUNCHMONEY_API
