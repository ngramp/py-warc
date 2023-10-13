import subprocess
import re


# Run the aws s3 ls command and capture the output
command = "aws s3 ls --recursive s3://commoncrawl/crawl-data/CC-NEWS/"
try:
    output = subprocess.check_output(command, shell=True, text=True)
except subprocess.CalledProcessError as e:
    print(f"Error running AWS CLI command: {e}")
    exit(1)


# Parse the output and extract WARC file URLs
warc_urls = []
for line in output.splitlines():
    match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \d+ (.+\.warc\.gz)', line)
    if match:
        warc_urls.append("s3://commoncrawl/" + match.group(1))


# Print the list of WARC file URLs
for url in warc_urls:
    print(url)