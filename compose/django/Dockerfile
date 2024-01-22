FROM python:3.9-buster
ENV PYTHONUNBUFFERED 1

# Update System
RUN apt-get update

RUN getent group django || groupadd -r django
RUN getent passwd django || useradd -r -g django django

COPY ../requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/django/start-backend.sh /start-backend.sh
RUN chmod +x /start-backend.sh && chown django /start-backend.sh

COPY . /app

WORKDIR /app
ENTRYPOINT ["/start-backend.sh"]