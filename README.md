# LinkedIn Job Data Extractor

This repository provides a Python script to extract and process job data from LinkedIn HTML files. It uses spaCy for Named Entity Recognition (NER) and regex patterns for structured data extraction.

## Features
- Extracts key information such as Company Name, Job Position, Location, Contract Type, Seniority, Industry, Management Skills, and On-site Days.
- Uses spaCy for language and salary detection.
- Processes downloaded HTML files to create a structured CSV dataset.

## Prerequisites
1. Python 3.8 or higher.
2. Dependencies:
   - `pip install -r requirements.txt`

### Required Libraries:
- `pandas`
- `beautifulsoup4`
- `html`
- `re`
- `spacy`
- `torch`
- Download spaCy's transformer model:
  ```bash
  python -m spacy download en_core_web_trf
  ```

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd linkedin-job-extractor
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Organize folders:
   - Place LinkedIn HTML files in the folder `all_jobs_html/`.

5. Run the script:
   ```bash
   python download_job_html.py
   ```

6. Check the output CSV file:
   ```bash
   job_data_with_spacy.csv
   ```

## Folder Structure
```
.
├── all_jobs_html/              # HTML files for job postings
├── applications_csv/           # Application-related CSV files
├── linkedin_curl               # Curl parameters (ignored)
├── download_job_html.py        # Main script
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── .gitignore                  # Ignore rules
```

## Notes
- Ensure the HTML files contain the required data for processing.
- The script supports extraction even if the HTML content structure varies slightly.
- For large datasets, consider optimizing the regex patterns or using parallel processing.

## License
This project is licensed under the MIT License.

