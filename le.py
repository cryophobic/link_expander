import csv
import re
import threading
from error_handler import ask_gpt
from modules.url_processing import expand_url, truncate_url
from utils import load_anim



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
        output_format = input("Enter a number: ")
        if output_format == '1':
            stop_event = threading.Event()
            animation_thread = threading.Thread(target=load_anim, args=(stop_event,))
            animation_thread.start()
            output_to_csv(urls)
            stop_event.set()
            animation_thread.join()
            break
        elif output_format == '2':
            stop_event = threading.Event()
            animation_thread = threading.Thread(target=load_anim, args=(stop_event,))
            animation_thread.start()
            output_to_txt(urls)
            stop_event.set()
            animation_thread.join()
            break
        elif output_format == '3':
            stop_event = threading.Event()
            animation_thread = threading.Thread(target=load_anim, args=(stop_event,))
            animation_thread.start()
            output_to_terminal(urls)
            stop_event.set()
            animation_thread.join()
            break
        else:
            print("Invalid input. Please enter 1, 2 or 3.")

    print("\rDone.")
