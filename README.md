# Voice Project

## Installation

If using `pipenv`:  
```
pipenv install --dev
```

Otherwise, create a virtual environment and run `pip install -r requirements.txt`.  

## Setup
Migrate the database with `python manage.py migrate`

Seed the database with `python manage.py seed`

Seeding the database will create various users. The username will be the user type followed by a sequence (ex. admin0, mentor0, mentor1, etc.). Mentors and admins can login with the password `password`. 

## Running
Run the server with `python manage.py runserver` and browse to the url `http://localhost:8000`.
