FROM ubuntu

# Install all generic software
RUN apt update
RUN apt install -y python3.10
RUN apt install -y python3-pip
RUN apt install -y nginx

# Install all python packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the Django project
COPY django/shrubbery /var/shrubbery

# Set up Nginx
ADD nginx.conf /etc/nginx/conf.d/default.conf

# Link nginx logs to container stdout
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# Expose the port
EXPOSE 80

# Prepare Gunicorn
RUN mkdir -pv /var/log/gunicorn/
RUN mkdir -pv /var/run/gunicorn/
COPY gunicorn_conf.py /var/shrubbery

# Copy start script and execute it
COPY start /var/shrubbery
RUN chmod +x /var/shrubbery/start
WORKDIR /var/shrubbery
CMD ["/bin/bash", "start"]
