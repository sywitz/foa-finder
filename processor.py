# processor.py

import pandas as pd
from datetime import datetime
from config import KEYWORDS_FILE, NONKEYWORDS_FILE

def to_date(date_str):
    """Convert date string from database into date object."""
    return datetime.strptime(date_str, '%Y%m%d').date()

def is_recent(date, days=14):
    """Check if date occurred within n amount of days from today."""
    return (datetime.today().date() - date).days <= days

def is_open(date_str):
    """Check if FOA is still open (close date is in the future)."""
    try:
        return datetime.today().date() <= to_date(date_str)
    except ValueError:
        return True  # Assume open if date is not parseable

def reformat_date(s):
    """Reformat the date string with hyphens to make it easier to read."""
    try:
        return datetime.strptime(s, '%Y%m%d').strftime('%Y-%m-%d')
    except ValueError:
        return s  # Return original if not parseable

def soup_to_df(soup):
    """Convert BeautifulSoup object from grants.gov XML into a DataFrame."""
    entries = [tag for tag in soup.find_all() if 'opportunitysynopsisdetail' in tag.name.lower()]
    data = {i: {child.name: child.text for child in entry.findChildren()} for i, entry in enumerate(entries)}
    df = pd.DataFrame.from_dict(data, orient='index')
    return df

def filter_by_dates_keywords(df):
    """Apply filters for recent dates and keywords."""
    if 'lastupdateddate' in df.columns:
        df['lastupdateddate'] = df['lastupdateddate'].apply(reformat_date)
        df = df[df['lastupdateddate'].apply(lambda x: is_recent(to_date(x)))]
    if 'closedate' in df.columns:
        df = df[df['closedate'].apply(is_open)]

    keywords = pd.read_csv(KEYWORDS_FILE, header=None)[0].str.lower().tolist()
    nonkeywords = pd.read_csv(NONKEYWORDS_FILE, header=None)[0].str.lower().tolist()
    df = df[df['description'].str.contains('|'.join(keywords), na=False)]
    df = df[~df['description'].str.contains('|'.join(nonkeywords), na=False)]

    df.sort_values(by='lastupdateddate', ascending=False, inplace=True)
    return df

def process_data(soup):
    """Process data from BeautifulSoup object to a filtered DataFrame."""
    df = soup_to_df(soup)
    if not df.empty:
        filtered_df = filter_by_dates_keywords(df)
        print('DataFrame sorted and filtered by date and keywords')
        return filtered_df
    else:
        print('No data found in XML')
        return pd.DataFrame()
