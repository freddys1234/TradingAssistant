
import smtplib
from email.mime.text import MIMEText
ADMIN_EMAIL = 'admin@yourdomain.com'

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'trading-bot@yourdomain.com'
    msg['To'] = to
    try:
        with smtplib.SMTP('smtp.yourmail.com', 587) as server:
            server.starttls()
            server.login('your-username', 'your-password')
            server.send_message(msg)
    except Exception as e:
        print(f'Failed to send email: {e}')

def send_admin_alert(subject, errors):
    body = '\n'.join(errors)
    send_email(ADMIN_EMAIL, subject, body)
