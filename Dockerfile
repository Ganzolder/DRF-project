FROM python:3.10.8-slim

WORKDIR /code

COPY ./requirements.txt .

# Установка Celery
RUN pip install celery

# Пример установки PostgreSQL в Dockerfile
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Запуск PostgreSQL
CMD service postgresql start && tail -f /dev/null

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
