# downloader.py

import os
import requests
from config import DOWNLOAD_DIR

def get_xml_url_and_filename():
    """Determine the URL and filename for the latest FOA database."""
    from datetime import datetime, timedelta

    day_to_try = datetime.today()
    file_found = None
    while not file_found:
        formatted_date = day_to_try.strftime('%Y%m%d')
        url = f'https://prod-grants-gov-chatbot.s3.amazonaws.com/extracts/GrantsDBExtract{formatted_date}v2.zip'
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            file_found = url
        else:
            day_to_try -= timedelta(days=1)

        filename = f'GrantsDBExtract{formatted_date}v2.zip'
    return url, filename

def download_file_from_url(url, filename):
    """Download the file from the given URL."""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f'Database downloaded to {filepath}')
    return filepath
