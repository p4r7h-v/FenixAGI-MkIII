import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def monitor_uptime(url, email_info):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            send_alert(email_info)
    except requests.RequestException as e:
        send_alert(email_info)

def send_alert(email_info):
    msg = MIMEMultipart()
    msg['From'] = email_info['from_email']
    msg['To'] = ', '.join(email_info['to_emails'])
    msg['Subject'] = 'Website is Down'
    body = 'Your website is down. Please check it out.'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(email_info['smtp_server'], email_info['smtp_port'])
    server.starttls()
    server.login(email_info['from_email'], email_info['password'])
    text = msg.as_string()
    server.sendmail(email_info['from_email'], email_info['to_emails'], text)
    server.quit()

email_info = {
    'from_email': 'your-email@gmail.com',
    'to_emails': ['recipient1@example.com', 'recipient2@example.com'],
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'password': 'your-email-password',
}

website = 'https://www.example.com'

monitor_uptime(website, email_info)