# Shrubbery
Web site for the Python course in FMI

### Install
* Clone the repository
* Create virtual env with...
  * requirements.txt installed
  * with DJANGO_SECRET_KEY set to a random ID (you can generate [here](https://djecrety.ir/)
  * with gmail username (GMAIL_USER) and password (GMAIL_PASS) set for yagmail (you can generate [here](https://myaccount.google.com/apppasswords)
* Start with python django/shrubbery/manage.py runserver 0.0.0.0:8080

### Deploy
* Inlcude the following env variables and external DB...
  * SHRUBBERY_ENV='prd'
  * POSTGRES_HOSTNAME
  * POSTGRES_USER
  * POSTGRES_PASSWORD
  * POSTGRES_DB_NAME