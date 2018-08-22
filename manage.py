#!/usr/bin/python

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
                print("Enter admin password : ", end="")
                admin_password = str(getpass.getpass())
                valid_username = bool(regex.match(USERNAME_REGEX, admin_username))
                if valid_username:
                    if create_admin(db, admin_username, admin_password):
                        print(
                            TERMINAL_COLORS['CRED'] + 
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
            print("Exiting Process")
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
    else:
        print(
            TERMINAL_COLORS['CRED'] + 
            "Unrecognised Command" + 
            TERMINAL_COLORS['CEND']
        )
elif len(sys.argv) == 1:
    user_instruction = """
    Below are list of available commands ->
    1) python manage.py create_admin 
    2) python manage.py commitall
    3) python manage.py dev
    """
    print(TERMINAL_COLORS['CBLUE']+user_instruction+TERMINAL_COLORS['CEND'])
else:
    print(
        TERMINAL_COLORS['CRED'] + 
        "Unrecognised Command" + 
        TERMINAL_COLORS['CEND']
    )