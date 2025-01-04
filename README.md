# LinkedIn Job Data Extractor

This repository provides Python scripts to download and process job data from LinkedIn HTML files. It uses spaCy for Named Entity Recognition (NER) and regex patterns for structured data extraction.

## Features
- Downloads job descriptions based on provided URLs and cookies.
- Extracts key information such as Company Name, Job Position, Location, Contract Type, Seniority, Industry, Management Skills, and On-site Days.
- Uses spaCy for language and salary detection.
- Processes downloaded HTML files to create a structured CSV dataset.

## Prerequisites
1. Python 3.8 or higher.
2. Install dependencies manually (no requirements.txt):
   ```bash
   pip install pandas beautifulsoup4 spacy torch
   python -m spacy download en_core_web_trf
   ```

## Process Overview
### 1. Download Job Applications
1. Go to [LinkedIn Data Download](https://www.linkedin.com/mypreferences/d/download-my-data).
2. Request and download your **LinkedIn Data Archive**.
3. Extract the ZIP file and locate the **Job Applications CSV files**.
4. Place the CSV files into a folder named `applications_csv/`.

### 2. Configure linkedin_curl File
1. Open a job listing on LinkedIn in your browser.
2. Press **F12** to open Developer Tools and navigate to the **Network** tab.
3. Refresh the page, and filter requests by **Doc** or **XHR**.
4. Right-click the request and select **Copy as cURL (bash)**.
5. Save the copied cURL command into a file named **linkedin_curl** in the root folder.
6. Make sure the cURL command includes the **cookies** from your browser session to authenticate requests.

### 3. Download Job Descriptions
1. Place the script **download_jobs.py** in the root folder.
2. Create a folder named **all_jobs_html/** to store downloaded job descriptions.
3. Run the script:
   ```bash
   python download_jobs.py
   ```
4. Confirm that job descriptions are saved in **all_jobs_html/**.

### 4. Extract Job Information
1. Place the script **extract_info.py** in the root folder.
2. Process the downloaded HTML files:
   ```bash
   python extract_info.py
   ```
3. Check the output CSV file:
   ```bash
   job_data_with_spacy.csv
   ```

## Folder Structure
```
.
├── all_jobs_html/              # HTML files for job postings
├── applications_csv/           # Application-related CSV files
├── linkedin_curl               # Curl parameters (ignored)
├── download_jobs.py            # Script for downloading job descriptions
├── extract_info.py             # Script for extracting information
├── README.md                   # Documentation
├── .gitignore                  # Ignore rules
```

## Notes
- Ensure the HTML files contain the required data for processing.
- The script supports extraction even if the HTML content structure varies slightly.
- For large datasets, consider optimizing the regex patterns or using parallel processing.

## License
This project is licensed under the MIT License.

