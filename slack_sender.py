# slack_sender.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_slack_text(df, filename):
    """Generate formatted text for sending to Slack."""
    db_date = filename.split('GrantsDBExtract')[1].split('v2')[0]
    db_date_formatted = f"{db_date[:4]}-{db_date[4:6]}-{db_date[6:]}"
    slack_text = f'Showing {len(df)} recently updated FOAs from grants.gov, extracted {db_date_formatted}:'
    slack_text += '\n======================================='

    base_hyperlink = 'https://www.grants.gov/search-results-detail/'

    for i, row in df.iterrows():
        hyperlink = base_hyperlink + row['opportunityid']
        slack_text += f"\n{i+1}) Updated: {row['updatedate']}, Closes: {row['closedate']}, Title: {row['opportunitytitle'].upper()} ({row['opportunityid']}) \n{hyperlink}"
        slack_text += '\n----------------------------------'

    return slack_text

def send_to_slack(slack_text):
    """Send the specified message to a Slack channel via a webhook."""
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps({'text': slack_text}), headers=headers)

    if response.status_code == 200:
        print('Message sent to Slack successfully.')
    else:
        print(f'Failed to send message to Slack: {response.status_code}, {response.text}')
