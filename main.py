import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
from datetime import datetime

# Setup logging for file/console
#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s - %(levelname)s - %(message)s',
#    handlers=[
#        logging.FileHandler('scraper_debug.log'), # File 
#        logging.StreamHandler()                   # Console
#    ]
#)

class AmazonScraper:
    def __init__(self):
        self.setup_driver()     # Handles Chrome
        self.file_index = 1     # Manages current output file
        self.counter = 0        # Tracks # of reviews

    def setup_driver(self):     
        # Setup Chrome driver
        options = webdriver.ChromeOptions()
        
        # Make browser more stable/stealthy
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
        # Manual login process done at start
        try:
            self.driver.get('https://www.amazon.com')
            input("Please log in to Amazon manually and press Enter when done...")
            logging.info("Login completed")
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")

    def extract_reviews(self, url):
        # Extract reviews from a single page
        try:
            logging.info(f"Processing URL: {url}")
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))  # Random delay just in case

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
                        #'timestamp': datetime.now().isoformat()
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
        # Save reviews to file
        if not reviews:
            logging.warning(f"No reviews to save for {url}")
            return

        try:
            filename = f'comments{self.file_index}.txt'
            with open(filename, 'a', encoding='utf-8') as file:
                
                #file.write(f"\nURL: {url}\n")
                #file.write(f"Timestamp: {datetime.now().isoformat()}\n")
                #file.write("-" * 40 + "\n")
                
                for review in reviews:
                    file.write(f"Review: {review['text']}\n")
                    file.write("-" * 40 + "\n")

            logging.info(f"Saved {len(reviews)} reviews to {filename}")
            
            self.counter += 1
            if self.counter % 10 == 0:      # 10 urls per txt file
                self.file_index += 1        # Increment

        except Exception as e:
            logging.error(f"Error saving reviews: {str(e)}")

    def run(self, urls_file):
        # Main exe method
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
                    
                    # Delay between URLs
                    time.sleep(random.uniform(1, 3))
                    
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




