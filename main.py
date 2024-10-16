# main.py

from huggingface_hub import InferenceClient

# Initialize the inference client with the model
client = InferenceClient(
    "microsoft/Phi-3-mini-4k-instruct",
    token="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",
)

# Open the prompts file and read the questions
with open("prompts.txt", "r") as prompts_file:
    prompts = prompts_file.readlines()

# Open the results file for writing
with open("results.txt", "w") as results_file:
    # Iterate through each prompt
    for prompt in prompts:
        # Strip whitespace and prepare the message
        message_content = prompt.strip()
        
        # Send the message to the model
        response = client.chat_completion(
            messages=[{"role": "user", "content": message_content}],
            max_tokens=500,
            stream=False,  # Set to False to get the full response at once
        )

        # Write the prompt and the response to the results file
        results_file.write(f"Prompt: {message_content}\n")
        results_file.write(f"Response: {response.choices[0].message['content']}\n\n")

print("Responses saved to results.txt")
