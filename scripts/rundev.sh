#!/bin/sh

gunicorn --worker-class eventlet run:app -w 1 --threads 12 || echo ERROR: Make sure you\'ve Gunicorn installed or you\'re in your virtual environment!