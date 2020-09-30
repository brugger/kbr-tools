import re
from typing import List

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
SMTP_TTL      = False

def login(server):
    if SMTP_PASSWORD is not None:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
    else:
        server.login(SMTP_USERNAME)

    return server

def is_valid_email(email: str):
    return re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None


class EmailAttachment:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path




def send_email( sender:str, recipients:list, subject:str, body:str, is_html:bool = False, attachments: List[EmailAttachment] = [], cc: list=[], bcc: list=[] ) -> None:

    if isinstance(recipients, str):
        recipients = [recipients]

    if isinstance(cc, str):
        cc = [cc]

    if isinstance(bcc, str):
        bcc = [bcc]

    msg = MIMEMultipart()
    msg.set_charset('UTF-8')
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Cc'] = ", ".join( cc )
    msg['Subject'] = subject
    body = body

    for att in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(att.path, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % att.name)
        msg.attach(part)


    if is_html:
        msg.attach(MIMEText(body,'html'))
    else:
        msg.attach(MIMEText(body,'plain'))

    addresses = recipients
    for x in cc:
        addresses.append(x)
    for x in bcc:
        addresses.append(x)

    text = msg.as_string()

    server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)

    if SMTP_TTL:
        server.starttls()

    if SMTP_USERNAME is not None:
        server = login( server )

    server.sendmail(sender, addresses, text)
    server.quit()

    return
