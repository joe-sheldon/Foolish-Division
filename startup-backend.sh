#!/bin/sh
#python manage.py runserver 0.0.0.0:8000
gunicorn --bind=0.0.0.0 \
  --reload \
  --workers=3 \
  foolish_division.wsgi:application