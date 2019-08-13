#!/bin/sh

gunicorn --reload --threads 3 -w 1 run:app || echo "\033[91mMake sure you've Gunicorn installed or you're in your virtual environment!\033[0m"