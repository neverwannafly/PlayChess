#!/usr/bin/env python

from PlayChess import create_admin, db, config

import re as regex
import sys
import subprocess
import getpass

USERNAME_REGEX = config.USERNAME_REGEX
TERMINAL_COLORS = config.TERMINAL_COLORS

if len(sys.argv) == 2:
    if sys.argv[1] == "create_admin":
        try:
            while True:
                print("Enter admin username : ", end="")
                admin_username = str(input())
                admin_password = str(getpass.getpass())
                valid_username = bool(regex.match(USERNAME_REGEX, admin_username))
                if valid_username:
                    if create_admin(db, admin_username, admin_password):
                        print(
                            TERMINAL_COLORS['CGREEN'] + 
                            "Admin added successfully to database!" + 
                            TERMINAL_COLORS['CEND']
                        )
                        break
                    else:
                        print(
                            TERMINAL_COLORS['CRED'] + 
                            "This username already exits! Please try again!" + 
                            TERMINAL_COLORS['CEND']
                        )
                else:
                    print(
                        TERMINAL_COLORS['CRED'] + 
                        "Such a username is invalid!" + 
                        TERMINAL_COLORS['CEND']
                    )
        except KeyboardInterrupt:
            print(
                TERMINAL_COLORS['CRED'] + 
                "Exiting Process" + 
                TERMINAL_COLORS['CEND']
            )
            sys.exit(1)
    elif sys.argv[1] == "dev":
        try:
            print(
                TERMINAL_COLORS['CBOLD'] + 
                TERMINAL_COLORS['CBLUE'] + 
                "Running Gunicorn with 12 Threads" +
                TERMINAL_COLORS['CEND'] + 
                TERMINAL_COLORS['CEND']
            )
            subprocess.call(['./app.sh', 'dev'])
        except KeyboardInterrupt:
            print(
                TERMINAL_COLORS['CRED'] + 
                "Exiting Server..." + 
                TERMINAL_COLORS['CEND']
            )
            sys.exit(1)
    elif sys.argv[1] == "prod":
        try:
            print(
                TERMINAL_COLORS['CBOLD'] + 
                TERMINAL_COLORS['CBLUE'] + 
                "Running Gunicorn with 12 Threads" +
                TERMINAL_COLORS['CEND'] + 
                TERMINAL_COLORS['CEND']
            )
            subprocess.call(['./app.sh', 'prod'])
        except KeyboardInterrupt:
            print(
                TERMINAL_COLORS['CRED'] + 
                "Exiting Server..." + 
                TERMINAL_COLORS['CEND']
            )
            sys.exit(1)
    elif sys.argv[1] == "local":
        config.IS_LOCAL = True
        try:
            print(
                TERMINAL_COLORS['CBOLD'] + 
                TERMINAL_COLORS['CBLUE'] + 
                "Running Local Instance" +
                TERMINAL_COLORS['CEND'] + 
                TERMINAL_COLORS['CEND']
            )
            subprocess.call(['./app.sh', 'dev'])
        except KeyboardInterrupt:
            print(
                TERMINAL_COLORS['CRED'] + 
                "Exiting Server..." + 
                TERMINAL_COLORS['CEND']
            )
            sys.exit(1)
    elif sys.argv[1] == "commitall":
        try:
            print(
                TERMINAL_COLORS['CBOLD'] + 
                TERMINAL_COLORS['CGREEN'] + 
                "Pushing changes to master branch and heroku..." +
                TERMINAL_COLORS['CEND'] + 
                TERMINAL_COLORS['CEND']
            )
            subprocess.call(['./app.sh', 'commitall'])
        except KeyboardInterrupt:
            print(
                TERMINAL_COLORS['CRED'] + 
                "Process Cancelled" + 
                TERMINAL_COLORS['CEND']
            )
            sys.exit(1)
    elif sys.argv[1] == "logs":
        try:
            print(
                TERMINAL_COLORS['CBOLD'] + 
                TERMINAL_COLORS['CGREEN'] + 
                "Opening Heroku logs......." +
                TERMINAL_COLORS['CEND'] + 
                TERMINAL_COLORS['CEND']
            )
            subprocess.call(['./app.sh', 'logs'])
        except KeyboardInterrupt:
            print(
                TERMINAL_COLORS['CRED'] + 
                "Closing Logs" + 
                TERMINAL_COLORS['CEND']
            )
            sys.exit(1)
    elif sys.argv[1] == "shell":
        try:
            print(
                TERMINAL_COLORS['CBOLD'] + 
                TERMINAL_COLORS['CGREEN'] + 
                "Starting Heroku Production Shell" +
                TERMINAL_COLORS['CEND'] + 
                TERMINAL_COLORS['CEND']
            )
            subprocess.call(['./app.sh', 'shell'])
        except KeyboardInterrupt:
            print(
                TERMINAL_COLORS['CRED'] + 
                "Closing Shell" + 
                TERMINAL_COLORS['CEND']
            )
            sys.exit(1)
    else:
        print(
            TERMINAL_COLORS['CRED'] + 
            "Unrecognised Command" + 
            TERMINAL_COLORS['CEND']
        )
elif len(sys.argv) == 1:
    user_instruction = """
    Below are list of available commands ->
    1) python manage.py create_admin    : Adds an admin
    2) python manage.py commitall       : Commits changes to both heroku and git repo.
    3) python manage.py dev             : Runs the development server
    4) python manage.py prod            : Runs the production server
    5) python manage.py shell           : Runs the production shell
    6) python manage.py logs            : Shows production logs
    """
    print(TERMINAL_COLORS['CBLUE']+user_instruction+TERMINAL_COLORS['CEND'])
else:
    print(
        TERMINAL_COLORS['CRED'] + 
        "Unrecognised Command" + 
        TERMINAL_COLORS['CEND']
    )