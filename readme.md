# PlayChess WebApp

## Current Features
<ul>
    <li>User registration</li>
    <li>User login</li>
    <li>User verification via emailID</li>
    <li>Admin login</li>
    <li>Creating new admin through command line
</ul>

## Check Points
These are the likely goals I would like to achieve in the near future
<ul>
    <li>Implement Admin dashboard and master control</li>
    <li>Implement necessary styling till now</li>
    <li><strong>A bit far :</strong> Make home page</li>
</ul>

## Adding a new admin!
There are two ways to add a new admin to website's database!
### Method 1 (Through the Interactive App):
--> Go to the home directory (where run.py is) through the terminal and enter the following code
```
$ source env/bin/activate #if virtual env isn't active
$ python3 new_admin.py
```
--> This will prompt you to type in your desired username and password!<br>
--> <strong>NOTE: </strong>your username can only contain alphanumeric characters and an underscore! Failing to adhere to username restrictions will result in error. However since you're in an interactive app, you will be reprompted to enter yoru username and password!

### Method 2 (Through the Script):
--> Go to the home directory (where run.py is) thorugh the terminal and enter the following code
```
$ source env/bin/activate #if virtual env isn't active
$ python3 new_admin.py <_ADMIN_USERNAME> <_ADMIN_PASSWORD>
```
--> You can type in your desired username followed by your desired password seperated by a space right in front of the python command!<br>
--> <strong>NOTE: </strong>In case of failure in creating an admin, it will throw an error and abort. It won't go for a reprompt and you'll need to run the command again!
## Testing the app
To test the current implementations of the app-><br>
--> Download the zip or fork the repo<br>
--> Go to the home directory(where run.py is) through terminal and run the following commands-><br>
```
$ source env/bin/activate
$ python3 run.py
```
--> goto localhost:5000/ on your browser and mendle around with the app!<br>
--> Do drop in your suggestions via pull requests <3 <br>

<hr></hr>

#### ~@Neverwannafly
