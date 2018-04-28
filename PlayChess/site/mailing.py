# Import configuration settings to send a verification email!
from . import config
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(id, email):
    try:
        email_conn = SMTP(config.configurations['host'], config.configurations['port'])
        email_conn.starttls()
        email_conn.login(config.configurations['username'], config.configurations['password'])
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Email verification"
        msg["From"] = config.configurations['username']
        msg["To"] = email
        plain_text = "Use " + str(id) + " as your verification code!"
        html_text = """
        <html>
            <body>
                <p> 
                    Hey! <br>
                    Please verify your email by entering the code below in verification prompt!<br>
                    """+ str(id) +"""
                </p>
            </body>
        </html>
        """
        part_1 = MIMEText(plain_text, "plain")
        part_2 = MIMEText(html_text, "html")
        msg.attach(part_1)
        msg.attach(part_2)
        email_conn.sendmail(config.configurations['username'], email, msg.as_string())
        email_conn.quit()
        return 1
    except SMTPException:
        return 0
