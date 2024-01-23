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
COPY ./compose/django/startup-dev.sh /startup-dev.sh
RUN chmod +x /startup-dev.sh && chown django /startup-dev.sh

# Copy Server files to /app directory
COPY . /app

# Expose Django API
EXPOSE 8000

WORKDIR /app
ENTRYPOINT ["/startup-dev.sh"]