# from smtplib import SMTP
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# SMTP_HOST = "localhost"
# SMTP_PORT = 1025
# SENDER_EMAIL = 'a2zhouseholdservices@email.com'
# SENDER_PASSWORD = ''

# def send_message(to, subject, content_body):
#     msg = MIMEMultipart()
#     msg["To"] = to
#     msg["Subject"] = subject
#     msg["From"] = SENDER_EMAIL
#     msg.attach(MIMEText(content_body, 'plain'))
#     client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
#     client.send_message(msg=msg)
#     client.quit()

# def send_report(to, subject, content_body):
#     msg = MIMEMultipart()
#     msg["To"] = to
#     msg["Subject"] = subject
#     msg["From"] = SENDER_EMAIL
#     msg.attach(MIMEText(content_body, 'html'))
#     client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
#     client.send_message(msg=msg)
#     client.quit()

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from contextlib import contextmanager

# SMTP server configuration
SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = 'a2zhouseholdservices@email.com'
SENDER_PASSWORD = ''

class EmailClient:
    """
    Handles email composition and sending operations
    """
    def __init__(self):
        self.host = SMTP_HOST
        self.port = SMTP_PORT
        self.sender = SENDER_EMAIL

    @contextmanager
    def _get_smtp_connection(self):
        """
        Context manager for handling SMTP connections
        """
        client = SMTP(host=self.host, port=self.port)
        try:
            yield client
        finally:
            client.quit()

    def _create_message(self, to, subject, content, content_type):
        """
        Creates a MIME message with specified parameters
        """
        msg = MIMEMultipart()
        msg["To"] = to
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg.attach(MIMEText(content, content_type))
        return msg

# Creating wrapper functions to maintain the same interface
def send_message(to, subject, content_body):
    """
    Sends a plain text email message using SMTP
    Args:
        to (str): Recipient email address
        subject (str): Email subject line
        content_body (str): Plain text message content
    """
    client = EmailClient()
    msg = client._create_message(to, subject, content_body, 'plain')
    with client._get_smtp_connection() as smtp:
        smtp.send_message(msg=msg)

def send_report(to, subject, content_body):
    """
    Sends an HTML formatted email report using SMTP
    Args:
        to (str): Recipient email address
        subject (str): Email subject line
        content_body (str): HTML formatted message content
    """
    client = EmailClient()
    msg = client._create_message(to, subject, content_body, 'html')
    with client._get_smtp_connection() as smtp:
        smtp.send_message(msg=msg)