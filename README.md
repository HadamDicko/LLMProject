# Sentiment Analysis for Product Reviews

## Overview
This project analyzes sentiment in product reviews using the Phi-3-mini-4k-instruct model from HuggingFace. It processes multiple files containing product reviews, determines the sentiment of each review (positive, negative, or neutral), and generates a visualization of the results.

## Features
- Processes multiple product review files simultaneously
- Sentiment analysis using HuggingFace's Phi-3-mini-4k-instruct model
- Generates sentiment results files for each product
- Creates a visual representation of sentiment distribution using matplotlib
- Handles errors gracefully with appropriate error messages
- Built-in input validation and data cleaning

## Requirements
- Python 3.7+
- Required packages:
  ```
  huggingface_hub
  matplotlib
  numpy
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HadamDicko/LLMProject/tree/Sentient-Analysis
   ```
   
2. Install required packages:
   ```bash
   pip install huggingface_hub matplotlib numpy
   ```

3. Set up HuggingFace authentication:
   - Create an account on HuggingFace
   - Generate an API token
   - Replace the `TOKEN` variable in the code with your token

## File Structure
```
project/
├── main.py                    # Main script
├── comments1.txt              # Product 1 reviews
├── comments2.txt              # Product 2 reviews
├── comments3.txt              # Product 3 reviews
├── comments4.txt              # Product 4 reviews
├── comments5.txt              # Product 5 reviews
└── sentiment_results{1-5}.txt # Generated results files
```

## Input File Format
Each comment file should follow this format:
```
Review: [review text]
Review: [review text]
----
Review: [review text]
```

## Usage
1. Prepare your review files following the input format above
2. Run the script:
   ```bash
   python main.py
   ```
3. The script will:
   - Process all review files
   - Generate sentiment result files
   - Display a bar graph showing sentiment distribution

## Output
1. Text Files:
   - Creates `sentiment_results{1-5}.txt` files
   - Each file contains sentiment labels for each review:
     ```
     Sentiment: positive
     Sentiment: negative
     Sentiment: neutral
     ```

2. Visualization:
   - Generates a bar graph showing:
     - Distribution of sentiments for each product
     - Color-coded bars (green=positive, gray=neutral, red=negative)
     - Numerical values for each sentiment category

## Functions
- `initialize_client()`: Sets up the HuggingFace client
- `read_comments()`: Reads and filters review comments
- `get_sentiment()`: Analyzes sentiment using the AI model
- `write_results()`: Saves sentiment analysis results
- `process_file()`: Orchestrates the analysis process
- `count_sentiments()`: Counts sentiment occurrences
- `create_sentiment_graph()`: Generates visualization

## Error Handling
The script includes error handling for:
- Missing input files
- API connection issues
- Invalid file formats
- Unexpected sentiment values

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Add your license information here]

## Contact
[Add your contact information here]
