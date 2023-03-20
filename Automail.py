import smtplib
import os
import schedule
import time
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

def send_email():
    # Set up the email parameters
    sender_email = 'senders email@gmail.com'
    sender_password = 'senders-email-password'
    receiver_email = 'receivers email@gmail.com'
    subject = 'Attendance Sheet'
    body = 'Please find attached the attendance sheet for today.'

    # Set up the Excel sheet attachment
    date_string = datetime.now().strftime("%Y-%m-%d")
    filename = f"attendance_{date_string}.xlsx"
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='xlsx')
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    if os.path.exists(filename):
        message.attach(attachment)

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Schedule the email to be sent at 6 PM
schedule.every().day.at("18:00").do(send_email)

# Keep running the script until the email is sent
while True:
    schedule.run_pending()
    time.sleep(1)
