# email_sender.py

import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

def create_email_text(df, filename):
    """Generate formatted text for email content."""
    db_date = filename.split('GrantsDBExtract')[1].split('v2')[0]
    db_date_formatted = f"{db_date[:4]}-{db_date[4:6]}-{db_date[6:]}"
    email_text = f'Here are the recently updated FOAs from grants.gov, extracted on {db_date_formatted}:\n\n'

    base_hyperlink = 'https://www.grants.gov/search-results-detail/'

    for i, row in df.iterrows():
        hyperlink = base_hyperlink + row['opportunityid']
        email_text += f"{i+1}) Update: {row['updatedate']}, Closes: {row['closedate']}, Title: {row['opportunitytitle'].upper()} ({row['opportunityid']})\n{hyperlink}\n\n"
    
    return email_text

def send_email(email_text):
    """Send the formatted email."""
    sender_address = os.getenv('SMTP_USER')
    sender_pass = os.getenv('SMTP_PASSWORD')
    receiver_address = 'sylashorowitz@gmail.com'  # Modify as needed
    subject = f'FOA Scrape for {datetime.now().strftime("%Y-%m-%d")}'

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    message.attach(MIMEText(email_text, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_address, sender_pass)
    server.sendmail(sender_address, receiver_address, message.as_string())
    server.quit()
    print(f'Email sent to {receiver_address}')
