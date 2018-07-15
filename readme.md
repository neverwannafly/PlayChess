# PlayChess WebApp

[![Build Status](https://travis-ci.org/neverwannafly/PlayChess.svg?branch=master)](https://travis-ci.org/neverwannafly/PlayChess)

## Current Features
<ul>
    <li>User registration and login</li>
    <li>User verification via emailID</li>
    <li>Admin dashboard</li>
    <li>Creating new admin through command line</li>
    <li>Functional chessboard with basic legal move check</li>
    <li>Unit testing</li>
</ul>

## Check Points
These are the likely goals I would like to achieve in the near future
<ul>
    <li>Implement necessary styling till now</li>
    <li>Make user profile page for logged in users</li>
    <li><strong>Castling/Enpassant/Pawn promotion</strong></li>
    <li><strong>Game room stacks for playing game</strong></li>
</ul>

## Hosting
Curently the live view of application is hosted on https://playchesswebsite.herokuapp.com/<br>
Feel free to check it out. <br>
NOTE: THIS FOR SOME REASONS DOESNT WORK!
Please check out issues and share your knowledge if you know a fix!

## <a name="env"></a>Setting up virtual env
#### For UNIX based devices(linux/mac)
<a id="#venv"></a>
To be able to run the project, you should either be having libraries mentioned in requirements.txt in your PC(The same version) or you can create your virtual env with all these libraries in few simple steps! (Recommended)<br>

```shell
$ python -m venv env # where env is name of our virtual environment
$ source env/bin/activate
$ (env) pip install -r requirements.txt
```
<hr></hr>

#### Windows 
Open windows power shell and change directory to the same as main directory of project (where readme.md is)<br>
Write in the following commands to set up your virtualenv

```shell
> pip install virtualenv # if virtualenv isn't installed
> virtualenv env # where env is name of virtual env
> env/Scripts/activate
> (env) pip install -r requirements.txt
```
<strong>NOTE: If you aren't able to activate the environment, you may need to change your execution policy. It's really simple, open powershell as an admin and write the following command -></strong>
```shell
> Set-ExecutionPolicy -ExecutionPolicy Unrestricted
```

## Adding a new admin!
There are two ways to add a new admin to website's database!
#### Method 1 (Through the Interactive App): 
<ul>
<li>Go to the main directory (where run.py is) through the terminal and enter the following code</li>
</ul>

```shell
$ python manage.py
```

<ul>
    <li>This will prompt you to type in your desired username and password!</li>
<li><strong>NOTE: </strong>your username can only contain alphanumeric characters and an underscore! Failing to adhere to username restrictions will result in error. However since you're in an interactive app, you will be reprompted to enter your username and password!</li>
</ul>

#### Method 2 (Through the Script):
<ul>
    <li>Go to the main directory (where run.py is) through the terminal and enter the following code</li>
</ul>

```shell
$ python manage.py <_ADMIN_USERNAME> <_ADMIN_PASSWORD>
```

<ul>
<li>You can type in your desired username followed by your desired password seperated by a space right in front of the python command!</li>
<li><strong>NOTE: </strong>In case of failure in creating an admin, it will throw an error and abort. It won't go for a reprompt and you'll need to run the command again!</li>
</ul>

## Different routes
<ul>
<li>The default url <strong>http://127.0.0.1:5000/</strong> or <strong>http://localhost:5000/</strong> routes to the site.</li>
<li>Use <strong>http://127.0.0.1:5000/admin/</strong> or <strong>http://localhost:5000/admin/</strong> to access the admin interface</li>
<li>Use <strong>http://127.0.0.1:5000/blog/</strong> or 
<strong>http://localhost:5000/blog/</strong> to access the blog interface</li>
<li><strong> NOTE : blog route is under development and encountering bugs is possible if you access the blog application. If you encounter any errors, please exit the application and start again! </strong></li>
</ul>

## Testing
Unit tests are written in Tests folder. You're free to add your own unit tests and improve app's
vulnerability to unwanted bugs on changes. To run unit tests, simply write the following 
command in command line -><br>
```shell
$ pytest
```
This would run all the unit tests present in files starting with prefix test*.py.<br>
#### Important notes while making unit tests
<ul>
<li> It's important for the test file and the testing methods to start with the prefix "test" for pytest to detect them and run the tests. </li>
<li> If you want to test on protected views, import login from client.py and and call login method before writing tests.
        
```python
from .client import login
from .client import client

def test_your_custom_view(client):
    login(client)
    # Now proceed with your tests
```
</li>

<li>If you want to test some functionality of chessboard which doesnt have a route, you can just import the chessboard class and perform tests on it

```python
from PlayChess import Chessboard
from .client import client

def test_chessboard(client):
    chessboard = Chessboard()
    # Now proceed testing this instance of Chessboard class
```
</li>

<li>You can also access the database in testing. Just import the db instance from PlayChess module

```python
from PlayChess import db
from .client import client

def test_database(client):
    # Now proceed with your tests.
    # To access database, just use this db instance (db is a PyMongo instance)
    # Eg-> To search a user, db.users.find_one({"username": "abc"})
```
</li>

</ul>

## Running the App
To run this flask app-><br>
<ul>
<li>Download the zip or fork the repo</li>
<li>Go to the main directory(where run.py is) through terminal and run the following commands-></li>

```shell
$ python run.py
```

<li>goto localhost:5000/ on your browser and mendle around with the app!</li>
<li>To exit the application, press Ctrl+C</li>
<li>Do drop in your suggestions via pull requests <3 </li>
<li>You can also run the app from gunicorn by using the following command and going to http://127.0.0.1:8000
    
```shell
$ gunicorn run:app
```
</ul>

## Import Closures

<ul>
<li> <h4>This project is only compatible with python3!</h4></li>
<li> <h4>If you encounter any bugs related to bcrypt library, make sure to have the same version as in requirnments.txt </h4></li>
<li> <h4><strong>NOTE: It's highly recommended to set up the virtual environment as described <a href="#env">here</a> </h4></strong></li>
</ul>

<hr>

#### ~@Neverwannafly
