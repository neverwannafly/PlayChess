# You can also pass arguments to this file to register a new admin!
# Note that you must pass valid arguments only!

from PlayChess import create_new_admin
import re as regex
import sys

USERNAME_REGEX = regex.compile("^[a-zA-Z0-9_]+$")

if len(sys.argv)==3:
    valid_username = bool(regex.match(USERNAME_REGEX, sys.argv[1]))
    if valid_username:
        if create_new_admin.createAdmin(sys.argv[1], sys.argv[2]):
            print("Admin added successfully to database!")
        else:
            print("This username already exits! Please try again!")
    else:
        print("Such a username is invalid!")
elif len(sys.argv)==1:
    while True:
        print("Enter admin username : ", end="")
        admin_username = str(input())
        print("Enter admin password : ", end="")
        admin_password = str(input())
        valid_username = bool(regex.match(USERNAME_REGEX, admin_username))
        if valid_username:
            if create_new_admin.createAdmin(admin_username, admin_password):
                print("Admin added successfully to database!")
                break
            else:
                print("This username already exits! Please try again!")
        else:
            print("Such a username is invalid!")
else:
    print("Invalid command!\n Make sure you're only passing username and password along with filename!")
    
