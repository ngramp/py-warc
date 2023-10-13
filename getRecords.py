import os
import time

import warcio
from bs4 import BeautifulSoup

from getEntities import hug_detect_named_entities

# from datasets import Dataset

# Directory containing downloaded WARC files
warc_dir = "warc_files"

# Profanity filter regex pattern
# profanity_pattern = re.compile(r"(profanity1|profanity2|profanity3)", re.IGNORECASE)


# Function to clean HTML content
def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style tags
    for script in soup(['script', 'style']):
        script.extract()
    # Extract and clean text content
    text_content = soup.get_text()
    # Remove excessive whitespace (including extra newlines and spaces)
    cleaned_content = ' '.join(text_content.split())
    return cleaned_content


# # Function to filter out excessive profanity
# def profanity_filter(text):
#     return not profanity_pattern.search(text)
#

# # Function to check for profanity
# def contains_profanity(text):
#     return bool(profanity_pattern.search(text))
#

# Function to iterate over WARC records in a file
def iterate_warc_records(file_path):
    i = 0
    with open(file_path, 'rb') as warc_file:
        data = []
        start_time2 = time.time()
        for record in warcio.archiveiterator.ArchiveIterator(warc_file):
            if record.rec_type == 'response':
                i = i + 1
                start_time1 = time.time()
                content = record.content_stream().read()
                # Handle decoding errors by replacing invalid characters
                cleaned_content = clean_html(content.decode('utf-8', errors='replace'))
                content_type = record.http_headers.get_header('Content-Type')
                if content_type and 'text/html' in content_type:
                    url = record.rec_headers.get_header('WARC-Target-URI')
                    text = cleaned_content
                    if url and text:
                        data.append({"url": url, "text": text})
                end_time1 = time.time()
                elapsed_time = end_time1 - start_time1
                # print(f"Elapsed time: {elapsed_time:.4f} seconds")
                if i % 100 == 0:
                    end_time2 = time.time()
                    elapsed_time2 = end_time2 - start_time2
                    average = elapsed_time2 / i
                    print(f"Elapsed time per 100: {elapsed_time2:.4f} seconds")
                    print(f"Average per 100: {average:.4f} seconds")
        print("total records: " + i)
        hug_detect_named_entities(data)
        # custom_dataset = Dataset.from_dict(data)


# Iterate over WARC files in the directory
for filename in os.listdir(warc_dir):
    print("here")
    if filename.endswith(".warc.gz"):
        warc_file_path = os.path.join(warc_dir, filename)
        print("Processing:", warc_file_path)
        iterate_warc_records(warc_file_path)
