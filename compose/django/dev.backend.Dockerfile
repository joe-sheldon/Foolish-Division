FROM python:3.9-buster
ENV PYTHONUNBUFFERED 1

# Update System
RUN apt-get update -yq 

# Set up Django user
RUN getent group django || groupadd -r django
RUN getent passwd django || useradd -r -g django django

# Install Python Requirements
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy Server files to /app directory, set init script to executable
COPY . /app
RUN chmod +x /app/startup-backend.sh && chown django /app/startup-backend.sh

# Expose Django API
EXPOSE 8000

WORKDIR /app
ENTRYPOINT ["/app/startup-backend.sh"]