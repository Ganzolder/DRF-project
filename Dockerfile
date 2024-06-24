FROM python:3.10.8-slim

WORKDIR /code

COPY ./requirements.txt .

# Запуск PostgreSQL
CMD service postgresql start && tail -f /dev/null

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
