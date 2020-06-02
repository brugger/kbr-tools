import smtplib

# Helper email modules
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# sender email address
sender = 'kim.brugger@uib.no

SMTP_SERVER = 'smtp.uib.no'
SMTP_PORT   = 25

def set_smtp_server( server:str, port:int=None):
    SMTP_SERVER = server

    if port is not None:
        SMTP_PORT = port



def send( sender:str, recipients:list, subject:str, body:str ) -> None:


    # sender email password for login purposes
    email_password = None

    # list of users to whom email is to be sent
    if isinstance( recipients, str ):
        recipients = [ recipients ]

    recipients = ['LIST_OF_RECIPIENTS']

    msg = MIMEMultipart()
    msg['From'] = sender
    # converting list of recipients into comma separated string
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body,'plain'))
    text = msg.as_string()
    server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    server.starttls()
#    server.login(sender, email_password)
    server.sendmail(sender, recipients, text)
    server.quit()


    return
