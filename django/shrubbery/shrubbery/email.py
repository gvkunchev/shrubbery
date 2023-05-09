import os
import yagmail


class Emailer:
    """Email."""

    SENDER = os.environ.get('GMAIL_USER')
    PASSWORD = os.environ.get('GMAIL_PASS')

    def __init__(self):
        """Initializator."""
        self._yag = yagmail.SMTP(self.SENDER, self.PASSWORD)

    def send_email(self, recipients, subject, body):
        """Send email."""
        self._yag.send(recipients, subject, body)
