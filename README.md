# Web Scraping Project

This project is designed to scrape product reviews from Amazon using Python. It utilizes libraries such as `requests`, `BeautifulSoup`, and `Selenium` to handle the scraping tasks, including CAPTCHA detection and handling.

## Features

- Scrapes product reviews from specified Amazon URLs.
- Automatically detects and allows for manual CAPTCHA solving.
- Saves scraped reviews to text files, organized by product.

## Requirements

Make sure to set up the environment using the provided `requirements.yml` file. This ensures that all necessary packages are installed.

### Requirements File

The project requires the following packages:
- `requests`: For making HTTP requests to fetch web pages.
- `beautifulsoup4`: For parsing HTML and extracting comments.
- `pandas`: Optional for data manipulation and analysis.
- `lxml`: For faster parsing with BeautifulSoup

## Setup Instructions

1. **Clone the repository and switch branch**:
   ```bash
   git clone [https://github.com/yourusername/yourrepository.git](https://github.com/HadamDicko/LLMProject/tree/webScrapping)
   cd LLMProject
   git checkout -b webScrapping
2. **Create the conda environment**:
   ```bash
   conda env create -f requirements.yaml
3. **Activate the environment**:
   ```bash
   conda activate webScraping-env
4. **Run the script**:
   ```bash
   python main.py
