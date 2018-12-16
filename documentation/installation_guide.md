# Installation manual

_Installation manual follows a process utilizing BASH (e.g. GitBash or other BASH emulator) in Windows_ 

## Local installation

Local machine requires 

- python3.x (with pip and venv)
- sqlite3

_In order to run the below commands python3.x and sqlite3 need to be configured in the Windows environment variables_

### Installation guide

1. Clone project to a local directory.

```
$ git clone git@github.com:roopekole/tsoha.git
```

Alternatively, the source code can be downloaded as a zip file from https://github.com/roopekole/tsoha.

2. Initiate virtual enviroment and initiate it
```
$ python -m venv venv
$ source venv/Scripts/activate
```

3. Install dependencies contained in requirements.txt

```
$ pip install -r requirements.txt
```

7. Run the application (application opens by default in http://localhost:5000)
```
$ python run.py
```

_GitHub repository contains a pre-populated database file. You may delete file or use it directly. If the file is deleted, the tables are created automatically_

**Create admin user**

First admin user needs to be inserted to the application database (by default application/theses.db)

_Ensure that admin is set to 1 and that userID has a structure of an email address (validated in the login input)_


```
$ sqlite3 application/theses.db 
sqlite> INSERT INTO account (userID, firstName, lastName, password, admin) VALUES ('admin@admin.com', 'adminFirst', 'adminLast', '$5$rounds=535000$yMpbShhzg.7X1/mp$pRXo2.pcc5X.6d7il39aGPgO89K/SZgyhr5oNSCG1Z/', 1);
```

_Passowrd needs to be sha256 encrypted and salted. Application is using passlib hashing. Sting can be hashed by_
```
$ python -c "from passlib.hash import sha256_crypt; print(sha256_crypt.hash('test'))";
```

## Deploying the application to Heroku

Deploying to Heroku requires the following

   1. Application has been installed according to the above specifications
   2. Heroku account has been created
   3. Heroku CLI (with env variables is installed)
   4. Requirements have not been added without adding them to requirements.txt

**Deployment steps**
   
1. Create a directory for the application
```
$ heroku create <project name>
```

2. Create Heroku project of the local application
```
$ git remote add heroku
$ git add .
$ git commit -m "Inital heroku commit"
$ git push heroku master
```

3. Add a database to heroku
```
$ heroku config:set HEROKU=1
$ heroku addons:add heroku-postgresql:hobby-dev
```

4. Create a first user
```
$ heroku pg:psql
::DATABASE=> INSERT INTO account ("userID", "firstName", "lastName", "password", "admin") VALUES ('admin@gmail.com', 'adminFirst', 'adminLast', '$5$rounds=535000$aNFMJXNyMUPXjgZm$wfsCerqK8Pfzl/2P5l.6BuPvTsqI1/Tv5QxjrGYhLq.', 1);
```
