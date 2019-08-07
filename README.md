web-security-training-project-for-developers
============================================

In the project you will learn pratical skills of searching for vulnerabilities and then creating fixes for them.

You will have a chance to get familiar with Angular and Django along the way.

Security is something we all should do more exercises and continuously extend our understanding in that area.


Story
-----

You work in world class security agency in defensive-programming department.
Today you have got new assignment.
For security reasons you are not shared any additional information about your client.

You are given the simple web chat application designed from the scratch. The application was designed
to enable secured and private communication for government top's officials. 

But your spy intelligence department has reported to you that the competetive agency from unfriendly party
intercepted transfer and managed to include unknown number of vulnerabilities, design flaws and backdoors in there so
it will enable to exploit the system and ruin that country.
The country is now in grave danger. This could lead to world destabilisation and military conflicts.

They attackers didn't left any trace and reverting is not possible.

You have to find all vulnerabilities in the application and remove them before deploy otherwise world future safety may be in question.

You don't have to worry about infrastructure your job is limited only to the web application functionality.


Training project
----------------

Welcome to the Forum app.

It consists 4 services:

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

How to run it?
--------------

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


