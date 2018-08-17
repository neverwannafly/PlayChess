#!/bin/sh

gunicorn --threads 12 -w 1 run:app || echo ERROR: Make sure you\'ve Gunicorn installed or you\'re in your virtual environment!