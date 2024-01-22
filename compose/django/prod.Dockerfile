FROM python:3.9-buster
ENV PYTHONUNBUFFERED 1

# Update System
RUN apt-get update

# Install NodeJS v18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs

# Set up Django user
RUN getent group django || groupadd -r django
RUN getent passwd django || useradd -r -g django django

# Install Python Requirements
COPY ../requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy CORRECT startup script
COPY ./compose/django/startup-prod.sh /startup-prod.sh
RUN chmod +x /startup-prod.sh && chown django /startup-prod.sh

# Copy Server files to /app directory
COPY . /app

# Install Node Modules
RUN cd /app/frontend && npm install

# Expose Frontend and Backend
EXPOSE 80 8000

WORKDIR /app
ENTRYPOINT ["/startup-prod.sh"]