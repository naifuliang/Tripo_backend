from django.apps import AppConfig
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class AuthorizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authorization"

def send_mail(address, theme, content):
    mail_host = "smtp.titan.email"
    mail_pass = "41bPqkX2jmdU#$lO"
    sender = "tripo@ilnf.space"

    receivers = [address]  # 收件人
    send_header = theme
    msg = MIMEMultipart()
    msg['Subject'] = send_header
    msg['From'] = sender
    msg['To'] = ",".join(receivers)
    msg.attach(MIMEText(content, _subtype='html', _charset='utf-8'))
    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(sender, mail_pass)
        server.sendmail(sender, receivers, msg.as_string())
        server.close()
        #     return True
    except Exception as e:
        print('email send fail', str(e))