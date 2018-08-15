#!/bin/sh

gunicorn run:app -w 1 --threads 12 || echo ERROR: Make sure you\'ve Gunicorn installed or you\'re in your virtual environment!