# Shrubbery
Web site for the Python course in FMI
[https://py-fmi.org/](https://py-fmi.org/)

### Develop
* Clone the repository
* Create virtual env with...
  * requirements.txt installed
  * (optional for email sends only) with gmail username (GMAIL_USER) and password (GMAIL_PASS) set for yagmail (you can generate [here](https://myaccount.google.com/apppasswords)
* Start with python django/shrubbery/manage.py runserver

### Deploy
* Create Posgre DB and set the following env variable for Shrubbery to access it
  * POSTGRES_HOSTNAME
  * POSTGRES_USER
  * POSTGRES_PASSWORD
  * POSTGRES_DB_NAME
* Set the global environment to production by setting the following env variable
  * SHRUBBERY_ENV='prd'
* Provide persistent data storage and mount it in /var/shrubbery/media
* Ensure that port 80 is redirected to the container
  * For example, render.com automatically scans ports serving HTTP. The current project serves HTTP over 80 and 8000 - 8000 is Gunicorn, while 80 is Nginx. You are required to use 80 in order to go through Nginx and serve media files. Serving through 8000 will go ardoun Ngninx and will not allow serving media files.

### Create new instance for the same container
* Create new settings_XXXX.py file in ./django/shrubbery
* Modify everything related to the year in that file
* Create new gunicorn_conf_XXXX.py file in ./
* Modify everything related to the year in that file
* Add new upstream in ./nginx.conf
* Add new server in ./nginx.conf
* Modify everything related to the year in these new configurations
* Modify the new server.server_name to use the plain domain (py-fmi.org) and alter the old one to XXXX.py-fmi.org
* Add a new line for every mention of an year in ./Dockerfile
* Add a new line for every mention of an year in ./start
* Create the new schema in the database:
  ```
  psql -h <host> -p <port> -U <username> <db_name> -W
  CREATE SCHEMA schemaXXXX;
  ```

