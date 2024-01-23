FROM python:3.9-buster
ENV PYTHONUNBUFFERED 1

# Update System
RUN apt-get update -yq

# Set up Django user
RUN getent group django || groupadd -r django
RUN getent passwd django || useradd -r -g django django

# Install Python Requirements
COPY ../requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy CORRECT startup script
COPY ./compose/django/startup-backend.sh /startup-backend.sh
RUN chmod +x /startup-backend.sh && chown django /startup-backend.sh

# Copy Server files to /app directory
COPY . /app

# Expose Frontend and Backend
EXPOSE 8000

WORKDIR /app
ENTRYPOINT ["/startup-backend.sh"]