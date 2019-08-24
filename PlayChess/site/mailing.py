# Import configuration settings to send a verification email!
from . import config
from smtplib import SMTP
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..utils import decorators

@decorators.disable
def sendMail(id, email, username):
    try:
        email_conn = SMTP(config.configurations['host'], config.configurations['port'])
        email_conn.starttls()
        email_conn.login(config.configurations['username'], config.configurations['password'])
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Email verification"
        msg["From"] = "playchesswebsite@gmail.com"
        msg["To"] = email
        plain_text = "Use " + id + " as your verification code!"
        html_text = """
        <html>
            <body>
                <p> 
                    Hey! <br>
                    Please use <br> {id} <br>as your verification code!
                </p>
            </body>
        </html>
        """.format(id=id)
        part_1 = MIMEText(plain_text, "plain")
        part_2 = MIMEText(html_text, "html")
        msg.attach(part_1)
        msg.attach(part_2)
        email_conn.sendmail(config.configurations['username'], email, msg.as_string())
        email_conn.quit()
        return 1
    except SMTPException:
        print("exc")
        return 0
