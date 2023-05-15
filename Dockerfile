FROM ubuntu

# Install all generic software
RUN apt update
RUN apt install -y python3.10
RUN apt install -y python3-pip

# Install all python packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the Django project
COPY django/shrubbery /var/shrubbery

# Expose the port
EXPOSE 80

# Prepare Gunicorn, migrate the DB and start 
RUN mkdir -pv /var/log/gunicorn/
RUN mkdir -pv /var/run/gunicorn/
COPY gunicorn_conf.py /var/shrubbery
COPY start /var/shrubbery
RUN chmod +x /var/shrubbery/start
WORKDIR /var/shrubbery
CMD ["/bin/bash", "start"]
