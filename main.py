# Rough Draft

# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer

# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer
model_name = "/Users/dazeddamo/Downloads/Phi-3-mini-4k-instruct-q4/"  # Path to model location
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to get model response
def get_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Read prompts from the text file
try:
    with open('prompts.txt', 'r') as file:
        prompts = file.readlines()
except FileNotFoundError:
    print("Error: prompts.txt not found.")
    prompts = []

# Store responses
responses = []
for prompt in prompts:
    response = get_response(prompt.strip())
    responses.append(response)
    print(f"Prompt: {prompt.strip()}\nResponse: {response}\n")  # Print responses for verification

# Write responses to responses.txt
try:
    with open('responses.txt', 'w') as file:
        for response in responses:
            file.write(response + "\n")
    print("Responses written to responses.txt successfully.")
except Exception as e:
    print(f"Error writing to responses.txt: {e}")


'''
# Load the model and tokenizer
model_name = "/Users/dazeddamo/Downloads/Phi-3-mini-4k-instruct-q4.gguf"  # Path to model location 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to get model response
def get_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Read prompts from the text file
with open('prompts.txt', 'r') as file:
    prompts = file.readlines()

# Store responses
responses = []
for prompt in prompts:
    response = get_response(prompt.strip())
    responses.append(response)

# Write responses to responses.txt
with open('responses.txt', 'w') as file:
    for response in responses:
        file.write(response + "\n")
'''
