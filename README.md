# StockIt
Create a new folder called ‘stockit’ in whatever location you’d like. This is your root folder. Open git bash inside this folder and enter:
```git clone https://github.com/SPriyanka0/CSC_490_CAPSTONE.git```

Enter your terminal and cd to this root folder/stockit i.e c:/users/afolder/stockit/stockit/
This location is the Angular frontend.

## Install node.js (v20.17.0 LTS)
```
# installs fnm (Fast Node Manager)
winget install Schniz.fnm

# configure fnm environment
fnm env --use-on-cd | Out-String | Invoke-Expression
(I have found that sometimes my terminal likes to ‘forget’ node/npm. It’s super annoying but this command here makes it remember it)

# download and install Node.js
fnm use --install-if-missing 20

# verifies the right Node.js version is in the environment
node -v # should print `v20.17.0`

# verifies the right npm version is in the environment
npm -v # should print `10.8.2`
```
After you install fnm, some of the following commands may not work. It required a terminal restart. If you get some ‘permission denied’ or stuff like that then enter this in terminal:
```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```

## Install Angular CLI
```npm install -g @angular/cli```

## Install Django
If you’ve never used python then you’ll have to install that
If you’re never used python then you’ll also have to install pip (a python library installer)

In terminal:
```
python -m pip install Django
pip install djangorestframework
pip install django-cors-headers
```




## Connecting DB
Install PostgreSQL (I assume everybody has done this already)
In terminal:
```
pip install psycopg2
pip install python-decouple
```
Open up psql - this is your SQL shell that comes installed with postgres.
It will prompt you for server, database, port and username - just hit enter for the defaults. It will then ask for your password - enter whatever you chose for your password. Then you’ll be connected to the default database. We’ll need to create a new one.

In psql:
```
	CREATE DATABASE stockit;
	GRANT ALL PRIVILEGES ON DATABASE stockit TO postgres;
```
On the grant all privileges command, ‘postgres’ is the default username. When you logged in, if your default username is different then use that instead.

You can list all databases by typing: \l
You can switch to the stockit database by typing: \c stockit

Navigate to your ‘backend’ folder. There is a file called ‘.env.example’. You can create a new file called ‘.env’ or edit this one so it is named that. Replace ‘your_password’ with your actual password to log into postgres. If your username is different, also change that. Host, port and db_name are already set. The actual file named .env is set on gitignore so we’re not pushing our own individual passwords.

Now that your database is set up, in terminal:
```
python manage.py migrate
python manage.py createsuperuser
```
Creating a super user prompts you for a username, email and password. This is creating your django admin credentials.

## THAT’S IT FOR SETUP

## To Start the Web Server
Frontend, in terminal:
```npm start ```
(note: ‘ng serve’ also works but there is a super annoying bug where you can’t ctrl+c the server process, you have to kill the terminal instead)

Backend, in terminal: 
```python manage.py runserver```

These servers need to both be running in separate terminals.

http://localhost:4200/  - displays the whole thing

http://localhost:8000/  - if you only want to access backend api requests

http://localhost:8000/admin - access the django admin panel, login using your superuser credentials

## Some Notes:
-If changes to the database schema are made then run:
 ```python manage.py makemigrations```
This creates a folder of the changes and can be pushed to the repo. 

After pulling from the repo, to update the schema you can run: 
```python manage.py migrate```
This updates the schema but doesn’t affect any actual data in the databases.

-Dumpdata and loaddata can be used to share database contents.

-For development, frontend and backend each have their own server that communicates. On deployment, this will change. 

(note to self: dont run with secret key and debug on in production, move to env)
