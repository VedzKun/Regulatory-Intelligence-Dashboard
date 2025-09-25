import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_dgft_public_notices(url):
    """
    Scrapes public notices from the DGFT Public Notices page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        notices = []
        # The notices are in a table with class 'table'
        table = soup.find('table', class_='table')
        if table:
            for row in table.find_all('tr')[1:]:  # Skip header
                cols = row.find_all('td')
                if len(cols) >= 4:
                    date = cols[1].get_text(strip=True)
                    subject_col = cols[2]
                    title = subject_col.get_text(strip=True)
                    link_tag = subject_col.find('a', href=True)
                    link = link_tag['href'] if link_tag else ''
                    if link and not link.startswith('http'):
                        link = f"https://www.dgft.gov.in{link}"
                    notices.append({
                        'Date': date,
                        'Title': title,
                        'Link': link
                    })
        else:
            print("Could not find notices table. Please check the page structure.")

        return notices

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

def update_data(file_path, new_data):
    """
    Saves new data to a CSV file, appending if the file already exists.
    """
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        new_df = pd.DataFrame(new_data)
        combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['Link'])
        combined_df.to_csv(file_path, index=False)
    else:
        new_df = pd.DataFrame(new_data)
        new_df.to_csv(file_path, index=False)

if __name__ == '__main__':
    dgft_portal_url = "https://www.dgft.gov.in/CP/?opt=public-notice"
    dgft_file_path = 'dgft_public_notices.csv'

    print(f"Starting data collection from DGFT: {dgft_portal_url}")
    dgft_scraped_data = scrape_dgft_public_notices(dgft_portal_url)

    if dgft_scraped_data:
        update_data(dgft_file_path, dgft_scraped_data)
        print(f"DGFT data successfully collected and saved to {dgft_file_path}")
    else:
        print("No DGFT data was collected. Please check the website URL and structure.")