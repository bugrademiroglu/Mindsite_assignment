# Mindsite Challenge
## About
That project creates and maintains long running jobs via REST API and it can be convertable to web app with frontend. User can create jobs, user can get detailed information about a specific job, user can create a user, user can list all the users, user can list last ten jobs, user can list only finished jobs, user can list only running jobs, user can cancel stop resume and restart the job.

In the project throttling was used in order to prevent high load and provide rate limit to end points.

## How it works
Accepts HTTP GET,POST Request
[You can see the api docs on!](https://mindsitechallenge.herokuapp.com/api/docs)
* You can cancel a specific job with using /canceljob/{int:job_id} (GET /api/canceljob/{int:job_id})
* You can create and start new job with using /createjob (POST /api/createjob/)
* You can get all the logs which were created before if you are curious with using /getalllogs (GET /api/getalllogs)
* You can get detailed log info about specified job with using /getdetailedjob/{int:job_id}  (PUT /api/getdetailedjob/{int:job_id})
* You can list all the finished jobs with using /getfinishedhjobs (GET /api/getfinishedhjobs/)
* You can list all the jobs with using /getjobs (GET /api/getjobs)
* You can get logs only for specified job with using /getlogs/{int:job_id} (GET /api/getlogs/{int:job_id})
* You can list specified user's last ten jobs according to the created date with using /lastjobs/{str:user_name} (GET /api/lastjobs/{str:user_name})
* You can restart a job which was failed or stopped by something with using /restart/{int:job_id} (GET /api/restart/{int:job_id})
* You can resume a stopped job with using /resumejob/{int:job_id} (GET /api/resumejob/{int:job_id})
* You can list all the running jobs with using /runningjobs (GET /api/runningjobs/)
* You can stop a specific job with using /stopjob/{int:job_id}  (GET /api/stopjob/{int:job_id})
* You can list and create users with using /userlist (GET - POST /api/userlist)

# Requirements
* asgiref==3.4.1
* attrs==21.2.0
* Django==3.2.6
* djangorestframework==3.12.4
* drf-spectacular==0.18.1
* importlib-metadata==4.8.1
* inflection==0.5.1
* jsonschema==3.2.0
* psutil==5.8.0
* psycopg2-binary==2.9.1
* pyrsistent==0.18.0
* pytz==2021.1
* PyYAML==5.4.1
* six==1.16.0
* sqlparse==0.4.1
* typing-extensions==3.10.0.2
* uritemplate==3.0.1
* zipp==3.5.0

## Technologies
In this project, For the backend language Python was used and Django and Django-Rest was used as a framework.
For the database, Sqlite was used.
## Installation and Run
To run the code:

###### On terminal:

Clone this repo
 ```bash
git clone git@github.com:bugrademiroglu/Mindsite_assignment.git
```

 ```bash
cd mindsite_assignment
pip install -r requirements.txt
python manage.py runserver
```

Alternately, to quickly try out this repo in the cloud, [You can access to project on heroku!](https://mindsitechallenge.herokuapp.com/api/docs/)

In order to test the project, type the following command on your terminal
```bash
python manage.py test
```
