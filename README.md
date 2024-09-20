# LLM Sentiment Analysis Project

## Hadam Dicko 

## Overview
This project utilizes the phi3-mini model to perform sentiment analysis on predefined prompts. The script reads user prompts from a file (`prompts.txt`), sends these prompts to the model, and writes the responses to an output file (`results.txt`).

## Setup Instructions
1. Clone the repository. (Only works when public)
   ```bash
   git clone https://github.com/HadamDicko/LLMProject
   cd LLMProject
3. Create a conda environment:
   ```bash
   conda env create -f requirements.yaml
4. Activate the enviroment
   ```bash
   conda activate phi3-env
5. Install HuggingFace
   ```bash
   pip install huggingface-hub
6. Run the main script
   ```bash
   python main.py 
