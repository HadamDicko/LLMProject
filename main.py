# Rough Draft

import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 

torch.random.manual_seed(0) 
model = AutoModelForCausalLM.from_pretrained( 
    "microsoft/Phi-3-mini-4k-instruct",  
    device_map="cuda",  
    torch_dtype="auto",  
    trust_remote_code=True,  
) 

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct") 

messages = [ 
    {"role": "system", "content": "You are a helpful AI assistant."}, 
    {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"}, 
    {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."}, 
    {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"}, 
] 

pipe = pipeline( 
    "text-generation", 
    model=model, 
    tokenizer=tokenizer, 
) 

generation_args = { 
    "max_new_tokens": 500, 
    "return_full_text": False, 
    "temperature": 0.0, 
    "do_sample": False, 
} 

output = pipe(messages, **generation_args) 
print(output[0]['generated_text'])




'''
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

#Second try

'''
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