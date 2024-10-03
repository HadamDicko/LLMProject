# LLM Sentiment Analysis Project

## Hadam Dicko 

## Overview
This project utilizes the phi3-mini model to perform sentiment analysis on predefined prompts. The script reads user prompts from a file (`prompts.txt`), sends these prompts to the model, and writes the responses to an output file (`results.txt`).

## Features
- **Prompt Handling**: Reads multiple questions from `prompts.txt`.
- **Model Interaction**: Utilizes the specified Hugging Face model (`microsoft/Phi-3-mini-4k-instruct`) for generating responses.
- **Output Management**: Saves the generated responses to `results.txt`, organizing them alongside their corresponding prompts.

## Setup Instructions
1. Clone the repository. (Only works when public)
   ```bash
   git clone https://github.com/HadamDicko/LLMProject
   cd LLMProject
2. Create a conda environment:
   ```bash
   conda env create -f requirements.yaml
3. Activate the enviroment
   ```bash
   conda activate phi3-env
4. Run the main script
   ```bash
   python main.py
5. Check Results
   ```bash
   cat results.txt
6. Debugging
   ```bash
   python --version
   sudo apt update
   sudo apt install python3 python3-pip

   ![Screenshot 2024-10-03 at 9 42 15 AM](https://github.com/user-attachments/assets/c408ab44-e045-4d09-9c73-1f6929d6d145)



