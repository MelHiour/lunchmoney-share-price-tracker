# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY stock-updater.py stock-updater.py
COPY config.yaml config.yaml

CMD [ "python3", "stock-updater.py"]
