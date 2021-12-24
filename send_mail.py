from Package import *

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(body,subject,receiver):

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = EMAIL_ADDRESS
    message['To'] = ','.join(receiver)

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, MAIL_PASSWORD)
    server.sendmail(message['From'], message['To'], msg_body)
    server.quit()