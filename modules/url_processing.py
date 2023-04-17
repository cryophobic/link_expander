# This module handles all the URL processing tasks and can be called independent of the main script

import json
import re
import requests
import urllib.parse
from bs4 import BeautifulSoup
from error_handler import ask_gpt

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
