from huggingface_hub import InferenceClient

# Initialize the inference client with the model
client = InferenceClient(
    "microsoft/Phi-3-mini-4k-instruct",
    token="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",
)

# Process comment files from 1 to 5
for file_num in range(1, 6):
    # Input and output file names
    input_file = f"comments{file_num}.txt"
    output_file = f"sentiment_results{file_num}.txt"
    
    try:
        # Read the comments from input file
        with open(input_file, "r") as comment_file:
            comments = comment_file.readlines()
        
        # Process comments and write results
        with open(output_file, "w") as results_file:
            for comment in comments:
                # Strip whitespace and prepare the message
                comment_text = comment.strip()
                
                # Skip empty lines and divider lines
                if not comment_text or comment_text.startswith('----'):
                    continue
                
                # Skip lines that don't start with "Review:"
                if not comment_text.startswith('Review:'):
                    continue
                
                # Remove "Review:" prefix for the analysis
                comment_text = comment_text[7:].strip()
                
                # Prepare the prompt for sentiment analysis
                prompt = f"Analyze the sentiment of this comment and respond with exactly one word (positive, negative, or neutral): '{comment_text}'"
                
                # Send the message to the model
                response = client.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    stream=False,
                )
                
                # Get the response and ensure it's one of the expected values
                sentiment = response.choices[0].message['content'].strip().lower()
                # Validate sentiment is one of the expected values
                if sentiment not in ['positive', 'negative', 'neutral']:
                    sentiment = 'neutral'  # Default to neutral if unexpected response
                
                # Write the comment and sentiment to the results file
                #results_file.write(f"Review: {comment_text}\n")
                results_file.write(f"Sentiment: {sentiment}\n\n")
                
        print(f"Processed {input_file} - Results saved to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")

print("Sentiment analysis complete!")



