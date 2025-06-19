#!/bin/bash

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start server
daphne -b 0.0.0.0 -p 8000 core.asgi:application