from huggingface_hub import InferenceClient
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np

def initialize_client(model_name: str, token: str) -> InferenceClient:
    """Initialize the HuggingFace inference client."""
    return InferenceClient(model_name, token=token)

def read_comments(filename: str) -> List[str]:
    """Read and filter valid comments from file."""
    try:
        with open(filename, "r") as file:
            comments = file.readlines()
            return [
                comment[7:].strip() # Remove "Review:" prefix
                for comment in comments
                if (comment.strip() and
                    not comment.strip().startswith('----') and
                    comment.strip().startswith('Review:'))
            ]
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        return []

def get_sentiment(client: InferenceClient, text: str) -> str:
    """Get sentiment prediction for a single comment."""
    prompt = f"Analyze the sentiment of this comment and respond with exactly one word (positive, negative, or neutral): '{text}'"
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            stream=False,
        )
        sentiment = response.choices[0].message['content'].strip().lower()
        # Validate sentiment
        return sentiment if sentiment in ['positive', 'negative', 'neutral'] else 'neutral'
    except Exception as e:
        print(f"Error getting sentiment: {str(e)}")
        return 'neutral'

def write_results(filename: str, results: List[Tuple[str, str]]) -> None:
    """Write sentiment analysis results to file."""
    try:
        with open(filename, "w") as file:
            for sentiment in results:
                file.write(f"Sentiment: {sentiment}\n\n")
    except Exception as e:
        print(f"Error writing to {filename}: {str(e)}")

def process_file(client: InferenceClient, input_file: str, output_file: str) -> None:
    """Process a single file for sentiment analysis."""
    comments = read_comments(input_file)
    if not comments:
        return
    results = [get_sentiment(client, comment) for comment in comments]
    write_results(output_file, results)
    print(f"Processed {input_file} - Results saved to {output_file}")

def count_sentiments(filename: str) -> dict:
    """Count the number of each sentiment type in a file."""
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('Sentiment:'):
                    sentiment = line.split(':')[1].strip().lower()
                    if sentiment in sentiments:
                        sentiments[sentiment] += 1
    except FileNotFoundError:
        print(f"Could not find file: {filename}")
    return sentiments

def create_sentiment_graph():
    """Create and display a bar graph of sentiment analysis results."""
    # Lists to store counts for each sentiment
    positives = []
    negatives = []
    neutrals = []
    
    # Read sentiment counts from each file
    for file_num in range(1, 6):
        filename = f"sentiment_results{file_num}.txt"
        counts = count_sentiments(filename)
        positives.append(counts['positive'])
        negatives.append(counts['negative'])
        neutrals.append(counts['neutral'])
    
    # Set up the bar graph
    products = [f'Product {i}' for i in range(1, 6)]
    width = 0.25
    x = np.arange(len(products))
    
    # Create bars
    plt.figure(figsize=(12, 6))
    plt.bar(x - width, positives, width, label='Positive', color='green', alpha=0.7)
    plt.bar(x, neutrals, width, label='Neutral', color='gray', alpha=0.7)
    plt.bar(x + width, negatives, width, label='Negative', color='red', alpha=0.7)
    
    # Customize the graph
    plt.xlabel('Products')
    plt.ylabel('Number of Reviews')
    plt.title('Sentiment Analysis Results by Product')
    plt.xticks(x, products)
    plt.legend()
    
    # Add value labels on top of each bar
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
    
    # Add value labels to all bars
    for bars in plt.gca().containers:
        add_value_labels(bars)
    
    # Adjust layout and display
    plt.tight_layout()
    plt.show()

def main():
    # Configuration
    MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
    TOKEN = "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"
    
    # Initialize client
    client = initialize_client(MODEL_NAME, TOKEN)
    
    # Process files
    for file_num in range(1, 6):
        input_file = f"comments{file_num}.txt"
        output_file = f"sentiment_results{file_num}.txt"
        process_file(client, input_file, output_file)
    
    print("Sentiment analysis complete!")
    
    # Create and display visualization
    print("\nGenerating visualization...")
    create_sentiment_graph()
    print("Visualization complete!")

if __name__ == "__main__":
    main()


