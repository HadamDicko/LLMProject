import requests
from bs4 import BeautifulSoup
import os

def fetch_comments(url):
    """Fetch comments from a specified URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Modify the selector based on the actual HTML structure of the page
        comments = soup.find_all(class_="user-comment")  # Example selector

        return [comment.get_text(strip=True) for comment in comments]
    except Exception as e:
        print(f"Error fetching comments from {url}: {e}")
        return []

def save_comments(version, comments):
    """Save comments to a file."""
    filename = f"comments_version{version}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for comment in comments:
            f.write(comment + "\n")
    print(f"Comments for version {version} saved to {filename}")

def main():
    # Read URLs from an input file
    with open("urls.txt", "r") as file:
        urls = file.readlines()

    # Iterate over each URL and fetch comments
    for i, url in enumerate(urls, start=1):
        url = url.strip()
        if url:  # Check if the URL is not empty
            comments = fetch_comments(url)
            if comments:
                save_comments(i, comments)

if __name__ == "__main__":
    main()
