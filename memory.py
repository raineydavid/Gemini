# open image_info.json and loop through the keys 
import openai
from ai import AI
from embedding import ask, compute_embeddings
import numpy as np
import pandas as pd
import json
from tqdm import tqdm
import yaml

# Load the configuration from the YAML file
with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Set the API key from the configuration
openai.api_key = config['openai']['api_key']

ai = AI(system=
"""You form memories given information about images. 
A memory is a 2 sentence summary of the image. Each memory starts with a date and location if present.
All your memories are in the first person, i.e I went to the beach.
You can add additional information to your memories if you want, but you should always be specific about the date and time, if you don't know it, just describe the memory as normal.
"""
,openai_module=openai)


# open image_knowledge.json and form a list of strings from each key
texts = []
with open('image_info.json') as f:
    data = json.load(f)
    for key in tqdm(data, desc="Generating memories"):
        image_info = data[key]
        response, messages = ai.generate_response(f'{image_info}', voice=False, clear_messages=True)
        texts.append(response)

df = compute_embeddings(texts)

# Save the DataFrame as a CSV
df.to_csv('memories.csv', index=False)



