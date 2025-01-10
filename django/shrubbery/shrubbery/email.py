import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

class Emailer:
    """Email."""

    SENDER = os.environ.get('GMAIL_USER')
    SENDER_ALIAS = 'noreply@py-fmi.org'
    PASSWORD = os.environ.get('GMAIL_PASS')

    def __init__(self):
        """Initializator."""
        pass

    def send_email(self, recipients, subject, body):
        """Send email."""
        return False # TODO: Remove after DB migration
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.SENDER, self.PASSWORD)
        message = MIMEMultipart()
        message['From'] = formataddr(('Python @ ФМИ', self.SENDER_ALIAS))
        message['To'] = self.SENDER_ALIAS
        message['Bcc'] = ','.join(recipients)
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))
        smtp.send_message(message)
        smtp.quit()
