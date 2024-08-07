FROM ubuntu:22.04

# Install all generic software
RUN apt update
RUN apt install -y python3.10
RUN apt install -y python3-pip
RUN apt install -y nginx
RUN apt install -y redis-server
RUN apt install -y mmdebstrap

# Install all python packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the Django project
COPY django/shrubbery /var/shrubbery

# Set up Nginx
ADD nginx.conf /etc/nginx/conf.d/default.conf

# Create directory for NginX log files
RUN mkdir -p /var/media/log

# Expose the port
EXPOSE 80

# Prepare Gunicorn
RUN mkdir -pv /var/log/gunicorn/
RUN mkdir -pv /var/run/gunicorn/
COPY gunicorn_conf.py /var/shrubbery

# Prepare sandbox for executing tests
RUN mkdir -p /var/shrubbery/sandbox/sandbox-origin
RUN mmdebstrap --variant=apt jammy /var/shrubbery/sandbox/sandbox-origin
COPY get-pip.py /var/shrubbery/sandbox/sandbox-origin/tmp
RUN chroot /var/shrubbery/sandbox/sandbox-origin apt update --allow-insecure-repositories
RUN chroot /var/shrubbery/sandbox/sandbox-origin apt install -y --allow-unauthenticated python3.10
RUN chroot /var/shrubbery/sandbox/sandbox-origin python3.10 /tmp/get-pip.py
RUN chroot /var/shrubbery/sandbox/sandbox-origin python3.10 -m pip install timeout_decorator
RUN useradd tester

# Copy start script and execute it
COPY start /var/shrubbery
RUN chmod +x /var/shrubbery/start
WORKDIR /var/shrubbery
CMD ["/bin/bash", "start"]
