import smtplib
from email.mime.text import MIMEText
from typing import List

FROM_ADDRESS = 'rothr96@gmail.com'
TO_ADDRESS = 'rothr96@gmail.com'


def send_email(passwd: str, msgs: List[str]) -> None:
    text = MIMEText('\n'.join(msgs))
    text['Subject'] = 'Notifications from auto scanner'
    text['From'] = FROM_ADDRESS
    text['To'] = TO_ADDRESS
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls() #enable security
    session.login(FROM_ADDRESS, passwd)
    # session = smtplib.SMTP('localhost', 1025)
    session.sendmail(FROM_ADDRESS, [TO_ADDRESS], text.as_string())
    session.quit()