import os
import requests
import time
import random
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Folders for organization
applications_folder = 'applications_csv'
html_folder = 'all_jobs_html'

# Ensure folders exist
os.makedirs(html_folder, exist_ok=True)

# Process all CSV files in the applications folder
csv_files = [f for f in os.listdir(applications_folder) if f.endswith('.csv')]
data = pd.concat([pd.read_csv(os.path.join(applications_folder, file)) for file in csv_files], ignore_index=True)

# Configure session with retry logic
session = requests.Session()
retry = Retry(
    total=5,                # Retry up to 5 times
    backoff_factor=1,       # Wait 1, 2, 4, 8, etc., seconds between retries
    status_forcelist=[429, 500, 502, 503, 504]  # Retry for these status codes
)
session.mount('https://', HTTPAdapter(max_retries=retry))

# Read cookies and headers from linkedin_curl file
def parse_curl_file(file_path):
    cookies = {}
    headers = {}
    with open(file_path, 'r') as file:
        lines = file.read().split('\\')  # Split by backslash for multi-line support
        for line in lines:
            line = line.strip().replace("'", "")  # Remove trailing spaces, quotes, and clean up
            if line.startswith('-H'):
                header = line[3:].split(': ', 1)  # Remove '-H ' and split
                if len(header) == 2:
                    key, value = header[0].strip(), header[1].strip()
                    if key.lower() == 'cookie':
                        # Parse cookies
                        cookie_items = value.split('; ')
                        for item in cookie_items:
                            if '=' in item:
                                k, v = item.split('=', 1)
                                cookies[k] = v
                    else:
                        headers[key] = value
    return cookies, headers

# Load cookies and headers
curl_file = 'linkedin_curl'
cookies, headers = parse_curl_file(curl_file)

# Function to download HTML content
def download_job_html(url, job_id):
    try:
        # Make request to fetch HTML with authentication cookies
        response = session.get(url, headers=headers, cookies=cookies)
        
        if response.status_code == 200:
            # Save HTML file
            file_path = os.path.join(html_folder, f'{job_id}.html')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Downloaded: {job_id}")
        else:
            print(f"Failed: {job_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {job_id}: {str(e)}")

# Loop through each job application and download HTML
for index, row in data.iterrows():
    job_url = row['Job Url']
    job_id = job_url.split('/')[-1]  # Extract job ID from URL

    # Avoid re-downloading existing files
    if not os.path.exists(os.path.join(html_folder, f'{job_id}.html')):
        download_job_html(job_url, job_id)
        
        # Add a random delay to reduce the risk of being rate-limited
        time.sleep(random.randint(5, 15))

print("Download process completed.")
