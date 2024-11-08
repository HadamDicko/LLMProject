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



""" Selenium based driver version (prints more output) """

"""
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_debug.log'),
        logging.StreamHandler()
    ]
)

class AmazonScraper:
    def __init__(self):
        self.setup_driver()
        self.file_index = 1
        self.counter = 0

    def setup_driver(self):
        """Setup Chrome driver with options"""
        options = webdriver.ChromeOptions()
        
        # Add options to make browser more stable/stealthy
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Add random user agent
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def login_to_amazon(self):
        """Manual login process"""
        try:
            self.driver.get('https://www.amazon.com')
            input("Please log in to Amazon manually and press Enter when done...")
            logging.info("Login completed")
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")

    def extract_reviews(self, url):
        """Extract reviews from a single page"""
        try:
            logging.info(f"Processing URL: {url}")
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))  # Random delay

            # Wait for reviews to load
            reviews = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-hook="review"]'))
            )

            extracted_reviews = []
            for review in reviews:
                try:
                    # Extract review body
                    review_body = review.find_element(By.CSS_SELECTOR, 'span[data-hook="review-body"]').text
                    
                    extracted_reviews.append({
                        'text': review_body,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    logging.error(f"Error extracting individual review: {str(e)}")
                    continue

            return extracted_reviews

        except TimeoutException:
            logging.error(f"Timeout waiting for reviews on {url}")
            return []
        except Exception as e:
            logging.error(f"Error processing URL {url}: {str(e)}")
            return []

    def save_reviews(self, reviews, url):
        """Save reviews to file"""
        if not reviews:
            logging.warning(f"No reviews to save for {url}")
            return

        try:
            filename = f'comments{self.file_index}.txt'
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(f"\nURL: {url}\n")
                file.write(f"Timestamp: {datetime.now().isoformat()}\n")
                file.write("-" * 40 + "\n")
                
                for review in reviews:
                    file.write(f"Review: {review['text']}\n")
                    file.write("-" * 40 + "\n")

            logging.info(f"Saved {len(reviews)} reviews to {filename}")
            
            self.counter += 1
            if self.counter % 10 == 0:
                self.file_index += 1

        except Exception as e:
            logging.error(f"Error saving reviews: {str(e)}")

    def run(self, urls_file):
        """Main execution method"""
        try:
            # First, handle login
            self.login_to_amazon()

            # Read URLs
            with open(urls_file, 'r') as file:
                urls = [line.strip() for line in file.readlines() if line.strip()]

            logging.info(f"Processing {len(urls)} URLs")

            for url in urls:
                try:
                    reviews = self.extract_reviews(url)
                    self.save_reviews(reviews, url)
                    
                    # Add a longer delay between URLs
                    time.sleep(random.uniform(5, 10))
                    
                except Exception as e:
                    logging.error(f"Error processing URL {url}: {str(e)}")
                    continue

        except Exception as e:
            logging.error(f"Error in main process: {str(e)}")
        finally:
            self.driver.quit()

def main():
    try:
        scraper = AmazonScraper()
        scraper.run('urls.txt')
    except Exception as e:
        logging.error(f"Critical error in main: {str(e)}")

if __name__ == "__main__":
    main()
"""




