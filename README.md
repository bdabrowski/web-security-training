sec-workshop
============

Welcome to the Forum app.

It consists from 4 services:

angularapp (frontend)
---------------------
The UI part of the forum having pages:

Forum list page: http://localhost:8080 
Forum details pages: http://localhost:8080/questions/1
Forum user page: http://localhost:8080/profile

djangoapp (backend)
-------------------
The backend part of the forum having pages:

Admin panel to manage data and approve questions: http://localhost:8080/admin/

Login and signup pages:

Login: http://localhost:8080/auth/login
Signup: http://localhost:8080/auth/signup

API:
Question API: http://localhost:8080/api/v1/forum/question/1
Answer API: http://localhost:8080/api/v1/forum/answer/1
Profile API: http://localhost:8080/api/v1/profile

legacyauditserver
-----------------
The legacy server used in past for logging. - (need to restart to run)



Start the app:

    docker-compose up
    
Stop to fill up database:

    docker-compose down
    
Build database schema:        
    
    docker-compose run --rm backend /bin/bash -c "python manage.py migrate --settings base.settings"
    
Populate database with test data:

    docker-compose run --rm backend /bin/bash -c "python manage.py populate --settings base.settings"

Create admin user:

    docker-compose run --rm backend /bin/bash -c "python manage.py createsuperuser --settings base.settings"
    
Run tests:

    docker-compose run --rm backend /bin/bash -c "python manage.py test --settings base.settings"
    
Start again:

    docker-compose up
    
Access front-end or admin page:

    http://localhost:8080/admin/ - admin page
    
    http://localhost:8080        - website


