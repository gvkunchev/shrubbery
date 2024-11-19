FROM ubuntu:24.10

# Install all generic software
RUN apt update
RUN apt install -y python3.12
RUN apt install -y python3-pip
RUN apt install -y python3-venv
RUN apt install -y nginx
RUN apt install -y redis-server
RUN apt install -y mmdebstrap
RUN apt install -y cargo
RUN apt install -y libpq-dev python3-dev

# Create and activate venv
RUN python3.12 -m venv /var/venv
ENV PATH="/var/venv/bin:$PATH"

# Install all python packages
COPY requirements.txt .
RUN python3.12 -m pip install -r requirements.txt

# Copy the Django project
RUN mkdir -p /var/shrubbery
COPY django/shrubbery /var/shrubbery/2023
RUN mv /var/shrubbery/2023/shrubbery/settings_2023.py /var/shrubbery/2023/shrubbery/settings.py
RUN mv /var/shrubbery/2024/shrubbery/settings_2024.py /var/shrubbery/2024/shrubbery/settings.py
COPY django/shrubbery /var/shrubbery/2024

# Prepare links for media
RUN ln -s /var/shrubbery/media/2023 /var/shrubbery/2023/media
RUN ln -s /var/shrubbery/media/2024 /var/shrubbery/2024/media

# Set up Nginx
ADD nginx.conf /etc/nginx/conf.d/default.conf

# Create directory for NginX log files
RUN mkdir -p /var/media/log

# Expose the port
EXPOSE 80

# Prepare Gunicorn
RUN mkdir -pv /var/log/gunicorn/
RUN mkdir -pv /var/run/gunicorn/
COPY gunicorn_conf_2023.py /var/shrubbery/2023
COPY gunicorn_conf_2024.py /var/shrubbery/2024

# Prepare sandbox for executing tests
RUN useradd tester
RUN mkdir -p /var/shrubbery/sandbox/sandbox-origin
RUN mmdebstrap --variant=apt noble /var/shrubbery/sandbox/sandbox-origin

# Clone user specs to the sandbox
RUN cp /etc/passwd /var/shrubbery/sandbox/sandbox-origin/etc/passwd
RUN cp /etc/group /var/shrubbery/sandbox/sandbox-origin/etc/group

# Prepare sandbox Python environment
COPY get-pip.py /var/shrubbery/sandbox/sandbox-origin/tmp
RUN chroot /var/shrubbery/sandbox/sandbox-origin apt update --allow-insecure-repositories
RUN chroot /var/shrubbery/sandbox/sandbox-origin apt install -y --allow-unauthenticated python3.12
RUN chroot /var/shrubbery/sandbox/sandbox-origin python3.12 /tmp/get-pip.py
RUN chroot /var/shrubbery/sandbox/sandbox-origin python3.12 -m pip install --break-system-packages timeout_decorator

# Copy start script and execute it
COPY start /var/shrubbery
RUN chmod +x /var/shrubbery/start
WORKDIR /var/shrubbery
CMD ["/bin/bash", "start"]
