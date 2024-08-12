# main.py

from downloader import get_xml_url_and_filename, download_file_from_url
from parser import unzip_and_soupify
from processor import process_data
from email_sender import create_email_text, send_email
from slack_sender import create_slack_text, send_to_slack

def main():
    url, filename = get_xml_url_and_filename()
    downloaded_file = download_file_from_url(url, filename)
    soup = unzip_and_soupify(downloaded_file)
    filtered_df = process_data(soup)

    # Create formatted text for Slack and email
    slack_text = create_slack_text(filtered_df, filename)
    email_text = create_email_text(filtered_df, filename)

    # Send messages
    send_email(email_text)
    send_to_slack(slack_text)

    print('Processed data sent both to email and Slack.')

if __name__ == '__main__':
    main()
