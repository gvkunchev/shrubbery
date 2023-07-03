import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer:
    """Email."""

    SENDER = os.environ.get('GMAIL_USER')
    SENDER_ALIAS = 'noreply@py-fmi.org'
    PASSWORD = os.environ.get('GMAIL_PASS')

    def __init__(self):
        """Initializator."""
        self._smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self._smtp.starttls()
        self._smtp.login(self.SENDER, self.PASSWORD)

    def send_email(self, recipients, subject, body):
        """Send email."""
        message = MIMEMultipart()
        message['From'] = self.SENDER_ALIAS
        message['To'] = self.SENDER_ALIAS
        message['Bcc'] = ','.join(recipients)
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))
        self._smtp.send_message(message)
