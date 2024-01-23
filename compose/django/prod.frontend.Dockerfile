FROM python:3.9-buster

# Update System
RUN apt-get update -yq \
    && curl -L https://deb.nodesource.com/setup_18.x | bash \
    && apt-get update -yq \
    && apt-get install -yq nodejs

# Copy CORRECT startup script
COPY ./compose/django/startup-frontend.sh /startup-frontend.sh
RUN chmod +x /startup-frontend.sh && chown django /startup-frontend.sh

# Copy Server files to /app directory
COPY . /app

# Install Node Modules
RUN cd /app/frontend && npm install

# Expose Frontend and Backend
EXPOSE 80

WORKDIR /app
ENTRYPOINT ["/startup-frontend.sh"]