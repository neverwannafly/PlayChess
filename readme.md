<p align="center"><img src="PlayChess/static/Images/logo/PlayChess.png" alt="PlayChess" height="150px"></p>

# PlayChess WebApp

[![Build Status](https://travis-ci.org/neverwannafly/PlayChess.svg?branch=master)](https://travis-ci.org/neverwannafly/PlayChess)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/neverwannafly/PlayChess.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/neverwannafly/PlayChess/alerts/)
[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/neverwannafly/PlayChess.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/neverwannafly/PlayChess/context:javascript)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/neverwannafly/PlayChess.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/neverwannafly/PlayChess/context:python)


## Features
<ul>
    <li>Admin dashboard</li>
    <li>User Dashboard</li>
    <li>Functional Chessboard</li>
    <li>Working Game Finding Mechanism</li>
    <li>Realtime Gameplay</li>
    <li>Engine evaluation at /api/stockfish</li>
    <li>Simple Global Chat at /chat</li>
</ul>

## Checkpoints
These are the likely goals that would be achieved in the near future (in order of decreasing priority)
<ul>
    <li>Pawn promotion</li>
    <li>Enforce End game condition</li>
    <li>Create a proper game lobby</li>
    <li>Make user profile page for logged in users</li>
    <li>Styling and more Functionality for Global Chat</li>
    <li>Store people's games and devise rating system</li>
</ul>

## Hosting
Curently the live view of application is hosted on https://playchesswebsite.herokuapp.com/<br>
Feel free to check it out. <br>

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

## Manage.py Script
This script is an easy interface to navigate through the webapp. Currently this script can create an admin, run  the development server and for individuals having access to heroku credentials (where the site is hosted), concurrently push changes to both origin and heroku branch at the same time. You can also see different interfaces of this script by just typing <strong>python manage.py</strong>. It's different interfaces are as follows->
#### Creating An Admin 

```shell
$ python manage.py create_admin
```

<ul>
    <li>This will prompt you to type in your desired username and password!</li>
<li><strong>NOTE: </strong>your username can only contain alphanumeric characters and an underscore! Failing to adhere to username restrictions will result in error. However since you're in an interactive app, you will be reprompted to enter your username and password!</li>
</ul>

#### Pushing Changes

```shell
$ python manage.py commitall
```

<ul>
<li>Now your changes would be pushed to both the heroku and the origin remotes</li>
</ul>

#### Checking Heroku Server Logs

```shell
$ python manage.py logs
```

<ul>
<li>It shows you the latest heroku logs of live server. You must be having the heroku credentials for this command to work</li>
</ul>

#### Running dev server


```shell
$ python manage.py dev
```

<ul>
<li>It'll start a dev Gunicorn server on port 8000</li>
<li><strong>NOTE: </strong>Donot use flask development server as it will only serve one client at a time and would only move to the second client when done with 1st. The game finding mechanism won't be able to execute.</li>
</ul>

#### Opening Production Shell

```shell
$ python manage.py shell
```

<ul>
<li>It opens the production shell</li>
</ul>

## Routes
<ul>
<li>The default url http://127.0.0.1:8000/ routes to the website's homepage.</li>
<li>Use http://127.0.0.1:8000/admin/ to access the admin interface</li>
<li>Use http://127.0.0.1:8000/blog/ to access the blog interface (NOT MADE)</li>
<li>Use http://127.0.0.1:8000/chat/ to access the global chat and chat with other players.</li>
<li>Use http://127.0.0.1:8000/api/stockfish to access the stockfish api.</li>
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
<li>Set up virtual env as prescribed</li>
<li>Get the .env file from owner of this repo and place it in correct directory</li>
<li>Go to the main directory(where manage.py is) through terminal and run the following command-></li>

```shell
$ python manage.py dev
```

<li>Goto <strong>http://127.0.0.1:8000/</strong> on your browser and play around around with the app!</li>
<li>To exit the application, press Ctrl+C</li>
<li>Do drop in your suggestions via pull requests <3 </li>

</ul>

## Import Closures

<ul>
<li> This project is only compatible with python3</li>
<li> Windows users will have trouble running manage.py script now, instead they can use-></li>
```shell
$ gunicorn --reload --threads 12 -w 1 run:app
```

<li>Documentation regarding certain aspects like chessboard class, stockfish api will be made available later</li>
</ul>

<hr>

#### ~@Neverwannafly
