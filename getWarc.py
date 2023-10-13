import os
import boto3
import time
from tqdm import tqdm

# List of WARC file URLs
warc_urls = [
    "s3://commoncrawl/crawl-data/CC-NEWS/2023/09/CC-NEWS-20230904222436-01038.warc.gz",
    "s3://commoncrawl/crawl-data/CC-NEWS/2023/09/CC-NEWS-20230904235352-01039.warc.gz",
    "s3://commoncrawl/crawl-data/CC-NEWS/2023/09/CC-NEWS-20230905014842-01040.warc.gz",
    # Add more URLs as needed
]

# Directory to save downloaded files
download_dir = "warc_files"
os.makedirs(download_dir, exist_ok=True)

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Rate limiting parameters
max_requests_per_second = 1  # Adjust this value as needed
request_interval = 1 / max_requests_per_second


# Function to download a single WARC file from S3 with progress feedback
def download_warc_with_progress(url, save_dir):
    try:
        filename = os.path.join(save_dir, os.path.basename(url))
        s3.download_file('commoncrawl', url.split('commoncrawl/')[1], filename)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url.split('commoncrawl/')[1]}: {str(e)}")


# Progress callback class for tqdm
class ProgressPercentage:
    def __init__(self, filename):
        self.filename = filename
        self.filesize = s3.head_object(Bucket='commoncrawl', Key=filename.split('commoncrawl/')[1])['ContentLength']
        self.progress_bar = tqdm(total=self.filesize, unit='B', unit_scale=True, desc=self.filename)

    def __call__(self, bytes_amount):
        self.progress_bar.update(bytes_amount)


# Iterate over the list of URLs and download the WARC files with rate limiting and progress feedback
for warc_url in warc_urls:
    download_warc_with_progress(warc_url, download_dir)
    time.sleep(request_interval)