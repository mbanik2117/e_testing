#!/bin/bash

# Apply migrations
sleep 5 && python manage.py makemigrations && python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django development server
celery -A test_setup worker -l info & python manage.py runserver 0.0.0.0:8000

sleep 2 && celery -A test_setup worker -l info &

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
