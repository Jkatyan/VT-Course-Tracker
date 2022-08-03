import keys
import smtplib
from email.mime.text import MIMEText

def email_alert(subject, body, to):
    # Account Sign-In
    username = keys.username
    password = keys.password

    # Prepare Email
    msg = MIMEText(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = username

    # Send Email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, to, msg.as_string())
    server.quit()

email_alert("test", "YO", "jaykatyan@gmail.com")


