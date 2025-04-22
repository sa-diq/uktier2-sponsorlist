import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

def download_sponsor_register():
    # Get the main page
    main_url = "https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers"
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the link to the latest register of licensed sponsors
    csv_link = None
    for link in soup.find_all('a', href=True):
        if 'Worker_and_Temporary_Worker.csv' in link['href']:
            csv_link = link['href']
            break
    if not csv_link:
        raise Exception("CSV link not found on the main page.")
    
    # Get the full URL for the CSV file
    csv_url = csv_link if csv_link.startswith('http') else 'https://www.gov.uk' + csv_link

    # Download the CSV file
    response = requests.get(csv_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download CSV file: {response.status_code}")
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"data/raw/sponsor_register_{today}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'wb') as file:
        file.write(response.content)

    print(f"Downloaded to {filename} from {csv_url}")
    return filename

if __name__ == "__main__":
    print("Starting download of sponsor register...")
    download_sponsor_register()
    print("Download complete.")
# This script downloads the latest register of licensed sponsors from the UK government website.

    