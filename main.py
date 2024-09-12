# Rough Draft

# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer
model_name = "path/to/phi3-mini"  # Adjust the path to your model's location
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
