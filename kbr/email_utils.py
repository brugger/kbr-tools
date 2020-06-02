import smtplib

# Helper email modules
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER   = 'smtp.uib.no'
SMTP_PORT     = 25
SMTP_USERNAME = None
SMTP_PASSWORD = None

def set_smtp_server( server:str, port:int=None):
    SMTP_SERVER = server

    if port is not None:
        SMTP_PORT = port


def set_username_password(username:str, password:str=None) -> None:
    SMTP_USERNAME = username

    if password is not None:
        SMTP_PASSWORD = password


def login(server):
    if SMTP_PASSWORD is not None:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
    else:
        server.login(SMTP_USERNAME)

    return server



def send( sender:str, recipients:list, subject:str, body:str, bcc:bool=False ) -> None:

    # sender email password for login purposes
    email_password = None

    # list of users to whom email is to be sent
    if isinstance( recipients, str ):
        recipients = [ recipients ]

    msg = MIMEMultipart()
    msg['From'] = sender
    # converting list of recipients into comma separated string
    msg['To'] = ", ".join(recipients)

    if bcc:
        msg['Bcc'] = ", ".join(recipients)
        msg['To'] = sender

    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body,'plain'))
    text = msg.as_string()
    server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    server.starttls()

    if SMTP_USERNAME is not None
        server = login( server )

    server.sendmail(sender, recipients, text)
    server.quit()

    return
