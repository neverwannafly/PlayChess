# PlayChess WebApp

## Current Features
<ul>
    <li>User registration and login</li>
    <li>User verification via emailID</li>
    <li>Admin login</li>
    <li>Creating new admin through command line</li>
    <li>Allow admins to create, delete and update users</li>
    <li>Functional chessboard (making moves only possible through CLI right now)
</ul>

## Check Points
These are the likely goals I would like to achieve in the near future
<ul>
    <li>Implement necessary styling till now</li>
    <li>Add check for legal/illegal moves</li>
    <li>Make chessboard functional through user clicks</li>
</ul>

## Hosting
Curently the live view of application is hosted on https://playchesswebsite.herokuapp.com/<br>
Feel free to check it out. 

## <a name="env"></a>Setting up virtual env
#### For UNIX based devices(linux/mac)
<a id="#venv"></a>
To be able to run the project, you should either be having libraries mentioned in requirements.txt in your PC(The same version) or you can create your virtual env with all these libraries in few simple steps! (Recommended)<br>

```
$ python -m venv env # where env is name of our virtual environment
$ source env/bin/activate
$ (env) pip install -r requirements.txt
```
<hr></hr>

#### Windows 
Open windows power shell and change directory to the same as main directory of project (where readme.md is)<br>
Write in the following commands to set up your virtualenv

```
> pip install virtualenv # if virtualenv isn't installed
> virtualenv env # where env is name of virtual env
> env/Scripts/activate
> (env) pip install -r requirements.txt
```
<strong>NOTE: If you aren't able to activate the environment, you may need to change your execution policy. It's really simple, open powershell as an admin and write the following command -></strong>
```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
```

## Adding a new admin!
There are two ways to add a new admin to website's database!
#### Method 1 (Through the Interactive App): 
<ul>
<li>Go to the main directory (where run.py is) through the terminal and enter the following code</li>
</ul>

```
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

```
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

## Testing the app
To test the current implementations of the app-><br>
<ul>
<li>Download the zip or fork the repo</li>
<li>Go to the main directory(where run.py is) through terminal and run the following commands-></li>

```
$ python run.py
```

<li>goto localhost:5000/ on your browser and mendle around with the app!</li>
<li>To exit the application, press Ctrl+C</li>
<li>Do drop in your suggestions via pull requests <3 </li>
</ul>

## Import Closures

<ul>
<li> <h4>This project is only compatible with python3!</h4></li>
<li> <h4>If you encounter any bugs related to bcrypt library, make sure to have the same version as in requirnments.txt </h4></li>
<li> <h4><strong>NOTE: It's highly recommended to set up the virtual environment as described <a href="#env">here</a> </h4></strong></li>
</ul>

<hr>

#### ~@Neverwannafly
