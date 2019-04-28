# Contains the configurations for sending a verification email!

import os

configurations = {
    'host': 'smtp.sendgrid.net',
    'port': 587,
    'username': 'apikey',
    'password': os.environ.get('SENDGRID_APIKEY', None),
}