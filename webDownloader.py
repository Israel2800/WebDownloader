#Testing project

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin

 
# Set the starting URL and maximum number of pages to download

start_url = 'https://www.example.com'
max_pages = 12

 

# Create a directory to store the website content

if not os.path.exists('website_content'):
    os.makedirs('website_content')

 

# Set up a set to store the visited URLs to avoid duplicates

visited_urls = set()

def download_page(url, depth=0):
    """Download a page and its linked pages and resources."""

    # Check if the maximum depth has been reached

    if depth > max_depth:
        return

 
    # Check if the URL has already been visited

    if url in visited_urls:
        return
    visited_urls.add(url)

 

    # Send a request to the website and get its HTML content

    response = requests.get(url)
    content = response.content

 

    # Save the website HTML content to a file

    parsed_url = urlparse(url)
    filename = parsed_url.netloc + parsed_url.path

    if filename.endswith('/'):
        filename += 'index.html'
    elif not '.' in filename.split('/')[-1]:
        filename += '/index.html'
    os.makedirs(os.path.join('website_content', os.path.dirname(filename)), exist_ok=True)
    with open(os.path.join('website_content', filename), 'wb') as f:
        f.write(content)

 

    # Parse the HTML content using BeautifulSoup and find all the links

    soup = BeautifulSoup(content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]

 

   # Download all the linked pages and resources

    for link in links:
        if not link:
            continue
        link = urljoin(url, link)
        parsed_link = urlparse(link)
        if parsed_link.netloc == parsed_url.netloc:
            download_page(link, depth=depth+1)
        else:

            # Follow external links recursively

            if parsed_link.scheme in ('http', 'https'):
                download_page(link, depth=depth+1)

 

# Start downloading the website content

download_page(start_url)