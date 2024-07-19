# Shrubbery
Web site for the Python course in FMI  
[https://djecrety.ir/](https://py-fmi.org/)

### Develop
* Clone the repository
* Create virtual env with...
  * requirements.txt installed
  * with DJANGO_SECRET_KEY set to a random ID (you can generate [here](https://djecrety.ir/)
  * with gmail username (GMAIL_USER) and password (GMAIL_PASS) set for yagmail (you can generate [here](https://myaccount.google.com/apppasswords)
* Start with python django/shrubbery/manage.py runserver 0.0.0.0:8080

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
