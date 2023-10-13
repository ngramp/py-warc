import os
import requests
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup

index_url = "https://data.commoncrawl.org/crawl-data/CC-NEWS/2023/08/"
save_dir = "~/warc_files"


# Function to download a single WARC file
def download_warc(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(save_dir, os.path.basename(urlparse(url).path))
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")


# Function to get a list of WARC file URLs from a CommonCrawl index page
def get_warc_urls():
    warc_urls = []
    try:
        response = requests.get(index_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.endswith(".warc.gz"):
                    warc_urls.append(href)
        else:
            print(f"Failed to fetch index page: {index_url}")
    except Exception as e:
        print(f"Error fetching index page {index_url}: {str(e)}")

    return warc_urls


# Function to count the number of WARC files in the directory
def count_warc_files(directory):
    return len([f for f in os.listdir(directory) if f.endswith(".warc.gz")])


# Main function to download WARC files sequentially
def main():
    os.makedirs(save_dir, exist_ok=True)
    print("getting warc urls")
    warc_urls = get_warc_urls()

    max_files = 3
    print("iterating over warc urls")
    for warc_url in warc_urls:
        while count_warc_files(save_dir) >= max_files:
            time.sleep(10)  # Pause for 10 seconds if the file count exceeds the limit
        print("downloading warc: " + warc_url)
        download_warc(warc_url)
        time.sleep(1)  # Add a delay to be respectful to the server


if __name__ == "__main__":
    main()