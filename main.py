import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# List of User-Agent strings
user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4894.117 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4855.118 Safari/537.36',
    # Add more User-Agents as needed
]

def check_captcha(soup):
    """Check if the page contains a CAPTCHA."""
    captcha_keywords = ["robot", "verification", "prove you are not a robot"]
    for keyword in captcha_keywords:
        if soup and keyword.lower() in soup.get_text().lower():
            return True
    return False

def solve_captcha(url):
    """Use Selenium to handle CAPTCHA challenges."""
    driver = webdriver.Chrome()  # Make sure ChromeDriver is in your PATH
    driver.get(url)
    
    # Pause to allow CAPTCHA to load and be solved manually
    print("CAPTCHA detected. Please solve it manually.")
    time.sleep(30)  # Adjust this as necessary for manual solving

    # After solving, get the page source
    html = driver.page_source
    driver.quit()
    return html

# Read URLs from 'urls.txt'
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines() if line.strip()]

# Initialize file index
file_index = 1
counter = 0

# Process each URL
for url in urls:
    # Select a random User-Agent
    user_agent = random.choice(user_agents)
    headers = {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US, en;q=0.5'
    }

    # Send a GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for CAPTCHA
        if check_captcha(soup):
            # If CAPTCHA is detected, solve it using Selenium
            html = solve_captcha(url)
            soup = BeautifulSoup(html, 'html.parser')  # Re-parse the page

        # Find all review elements
        reviews = soup.find_all('div', {'data-hook': 'review'})

        # Open the appropriate comments file
        with open(f'comments{file_index}.txt', 'a', encoding='utf-8') as file:
            # Extract and write each review's details to the file
            for review in reviews:
                title = review.find('a', {'data-hook': 'review-title'}).get_text(strip=True)
                body = review.find('span', {'data-hook': 'review-body'}).get_text(strip=True)
                reviewer_name = review.find('span', class_='a-profile-name').get_text(strip=True)
                review_date = review.find('span', {'data-hook': 'review-date'}).get_text(strip=True)

                # Write review details to file
                file.write(f"Reviewer: {reviewer_name}\n")
                file.write(f"Review Title: {title}\n")
                file.write(f"Review Body: {body}\n")
                file.write(f"Review Date: {review_date}\n")
                file.write("-" * 40 + "\n")

        # Increment the counter
        counter += 1

        # Increment file index every 3 URLs
        if counter % 5 == 0:
            file_index += 1
    else:
        print(f"Failed to retrieve page: {response.status_code} for URL: {url}")





