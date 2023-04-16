# This script is a URL expander and formatter that takes a list of shortened URLs as input, expands them to their original long URLs, and outputs the results in a user-selected format (CSV, TXT, or terminal). 
#The script follows these main steps:

# Accepts user input of multiple shortened URLs and an 'END' keyword to stop receiving input.
# Processes each URL using the expand_url function, which sends a request to the httpstatus API to retrieve the expanded URL and its associated title.
# If any error occurs while expanding the URL, the script calls the ask_gpt3 function from the gpt3_error_handler module to provide suggestions on how to fix the issue.
# Processes the expanded URLs using the truncate_url function, which simplifies YouTube URLs by extracting video or playlist IDs and removes query strings for non-YouTube URLs.
# Outputs the processed URLs in the user-selected format (CSV, TXT, or terminal).
# This script provides an efficient way to expand and format a list of shortened URLs, making it easier to manage and analyze the original long URLs.

import csv
import json
import re
import requests
import urllib.parse
from bs4 import BeautifulSoup
from gpt3_error_handler import ask_gpt3
from utils import load_anim

def expand_url(short_url):
    # Sends a GET request to the shortened URL and follows redirects using httpstatus API
    headers = {'Content-Type': 'application/json'}
    data = {'requestUrl': short_url}
    response = requests.post('https://api.httpstatus.io/v1/status', headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            result = json.loads(response.content)
            chain = result['response']['chain']
            expanded_url = chain[-1]['url']

            # Send a request to the expanded URL and parse the HTML content
            page_response = requests.get(expanded_url)
            if page_response.status_code == 200:
                soup = BeautifulSoup(page_response.content, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.text.strip()
                else:
                    title = ''
                    print(f"Warning: Title tag is missing in the HTML content for URL {expanded_url}.")
            else:
                title = ''
                print(f"Warning: Unable to retrieve the HTML content for URL {expanded_url}. HTTP {page_response.status_code}")

            return expanded_url, title
        except Exception as e:
            error_description = f"Error expanding URL: {short_url} - {str(e)}"
            print(error_description)
            gpt3_suggestions = ask_gpt3(error_description)
            print("GPT-3 suggestions:")
            print(gpt3_suggestions)
            return None, None
    else:
        print(f"Error expanding URL: {short_url} - HTTP {response.status_code}")
        print(f"JSON response: {response.content.decode('utf-8')}")
        return None, None

def truncate_url(expanded_url):
    # Parses the expanded URL to extract components
    parsed_url = urllib.parse.urlparse(expanded_url)

    # Handles YouTube links
    if 'youtube.com' in parsed_url.netloc or 'youtu.be' in parsed_url.netloc:
        # Parses the query parameters
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Handles YouTube videos
        video_id = query_params.get('v', None)
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id[0]}"

        # Handles YouTube playlists
        playlist_id = query_params.get('list', None)
        if playlist_id:
            return f"https://www.youtube.com/playlist?list={playlist_id[0]}"

        return expanded_url

    # Truncates non-YouTube URLs by removing query strings
    pattern = re.compile(r'(\?.*|\/\?.*)')
    return pattern.sub('', expanded_url)

def output_to_csv(urls):
    # Outputs the URLs to a CSV file
    with open('output/urls.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Short URL', 'Expanded URL', 'Truncated URL'])
        for short_url in urls:
            expanded_url, title = expand_url(short_url)
            if expanded_url:
                truncated_url = truncate_url(expanded_url)
                writer.writerow([title, short_url, expanded_url, truncated_url])
            else:
                writer.writerow([title, short_url, 'Error expanding URL', ''])
    print("CSV output saved to urls.csv")

def output_to_txt(urls):
    # Outputs the URLs to a text file with each URL escaped to a new line
    with open('output/urls.txt', 'w') as txtfile:
        for short_url in urls:
            expanded_url, title = expand_url(short_url)
            if expanded_url:
                truncated_url = truncate_url(expanded_url)
                txtfile.write(title + ': ' + truncated_url + '\n')
    print("Text output saved to urls.txt")

def output_to_terminal(urls):
    # Outputs the URLs to the terminal
    for short_url in urls:
        expanded_url, title = expand_url(short_url)
        if expanded_url:
            truncated_url = truncate_url(expanded_url)
            print(f"{title}: {truncated_url}")
        else:
            print(f"{short_url}: Error expanding URL")

if __name__ == '__main__':
    # Prompts the user to paste URLs and type 'END' on a new line when done
    print("Please paste your URLs and type 'END' on a new line when done:")

    # Read input from the user
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)

    # Join the input lines into a single string
    url_text = ' '.join(lines)

    # Split the URL text into a list of URLs
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url_text)

    # Prompts the user to choose an output format
    print("Please choose an output format:")
    print("1) CSV")
    print("2) TXT")
    print("3) Terminal")
  
    while True:
        load_anim()
        output_format = input("Enter a number: ")
        if output_format == '1':
            output_to_csv(urls)
            break      
        elif output_format == '2':
            output_to_txt(urls)
            break
        elif output_format == '3':
            output_to_terminal(urls)
            break
        else:
            print("Invalid input. Please enter 1, 2 or 3.")

    print("\rDone.")
