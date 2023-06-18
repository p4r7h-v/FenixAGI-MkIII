import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def start_email_campaign(sender_email, sender_password, subject, message, recipient_emails):
    # Create a SMTP session
    server = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Start TLS for security
    server.starttls()

    # Authentication
    server.login(sender_email, sender_password)
    
    # Send email to each recipient
    for recipient_email in recipient_emails:
        # Create a message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attaching message 
        msg.attach(MIMEText(message, 'plain'))
        
        # Finally send the mail
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)

    # close the SMTP session
    server.quit()