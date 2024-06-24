FROM python:3.10.8-slim

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
