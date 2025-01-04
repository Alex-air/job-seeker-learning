import os
import pandas as pd
from bs4 import BeautifulSoup
import html
import re
import spacy

# Folders
html_folder = 'all_jobs_html'
output_file = 'job_data_with_spacy.csv'

# Initialize list to store job data
job_data = []

# Load spaCy's transformer model
nlp = spacy.load("en_core_web_trf")

# Extract job description from raw HTML
def extract_job_description(html_content):
    start_tag = 'com.linkedin.pemberly.text.Attribute&quot;}],&quot;text&quot;:&quot;'
    end_tag = '&quot;repostedJobPosting&quot;:null'
    match = re.search(f'{re.escape(start_tag)}(.*?){re.escape(end_tag)}', html_content)
    if match:
        return html.unescape(match.group(1))
    return 'Not Available'

# Extract company name from raw HTML
def extract_company_name(html_content):
    match = re.search(r'fs_normalized_company:\d+&quot;,&quot;name&quot;:&quot;(.*?)&quot;', html_content)
    if match:
        return html.unescape(match.group(1))
    return 'Not Available'

# Extract job position from raw HTML
def extract_job_position(html_content):
    match = re.search(r'repostedJobPosting&quot;:null,&quot;title&quot;:&quot;(.*?)&quot;', html_content)
    if match:
        return html.unescape(match.group(1))
    return 'Not Available'

# Extract location from raw HTML
def extract_location(html_content):
    match = re.search(r'&quot;defaultLocalizedName&quot;:&quot;(.*?)&quot;', html_content)
    if match:
        return html.unescape(match.group(1))
    return 'Not Available'

# Extract contract type from raw HTML
def extract_contract_type(html_content):
    match = re.search(r'&quot;description&quot;:\[\{&quot;text&quot;:\{&quot;textDirection&quot;:&quot;USER_LOCALE&quot;,&quot;text&quot;:&quot;(.*?)&quot;', html_content)
    if match:
        return html.unescape(match.group(1))
    return 'Not Available'

# Infer seniority level
def infer_seniority(job_description):
    keywords = ["junior", "mid-level", "senior", "lead", "manager", "director"]
    for word in keywords:
        if word in job_description.lower():
            return word.capitalize()
    return 'Not Available'

# Infer company's industry
def infer_industry(job_description):
    keywords = ["finance", "technology", "healthcare", "gaming", "education", "marketing"]
    for word in keywords:
        if word in job_description.lower():
            return word.capitalize()
    return 'Not Available'

# Detect management skills
def detect_management_skills(job_description):
    if any(word in job_description.lower() for word in ["team management", "leadership", "supervision"]):
        return 'Yes'
    return 'No'

# Detect on-site days
def detect_onsite_days(job_description):
    keywords = ["remote", "hybrid", "on-site"]
    for word in keywords:
        if word in job_description.lower():
            return word.capitalize()
    return 'Not Available'

# Extract entities using spaCy with focus on first match and filtering noise
def extract_entities(text):
    doc = nlp(text)
    entities = {
        'LANGUAGE': [], # Languages
        'MONEY': []     # Salary
    }

    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)

    # Cleanup noisy data by focusing on first match
    for key in entities:
        if entities[key]:
            entities[key] = entities[key][0]  # Prioritize the first match
        else:
            entities[key] = 'Not Available'

    return entities

# Function to extract job info using spaCy
def extract_job_info(html_content):
    # Extract fields
    company_name = extract_company_name(html_content)
    job_position = extract_job_position(html_content)
    job_description = extract_job_description(html_content)
    location = extract_location(html_content)
    contract_type = extract_contract_type(html_content)

    # Use spaCy to extract structured data
    entities = extract_entities(job_description)

    # Infer additional details
    seniority = infer_seniority(job_description)
    industry = infer_industry(job_description)
    management_skills = detect_management_skills(job_description)
    onsite_days = detect_onsite_days(job_description)

    # Return structured data
    return {
        'Company Name': company_name,
        'Job Position': job_position,
        'Location': location,
        'Contract Type': contract_type,
        'Seniority': seniority,
        'Industry': industry,
        'Management Skills': management_skills,
        'On-site Days': onsite_days,
        'Languages Requested': entities['LANGUAGE'],
        'Salary': entities['MONEY'],
        'Description': job_description
    }

# Process all HTML files
print("Starting processing of HTML files...")
for filename in os.listdir(html_folder):
    if filename.endswith('.html'):
        print(f"Processing file: {filename}")
        file_path = os.path.join(html_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            job_info = extract_job_info(html_content)
            job_info['File Name'] = filename
            job_data.append(job_info)

print("Finished processing all files.")

# Save data to CSV
print("Saving data to CSV...")
df = pd.DataFrame(job_data)
df.to_csv(output_file, index=False)

print(f"Extraction complete. Data saved to {output_file}")
