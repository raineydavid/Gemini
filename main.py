from embedding import ask
import pandas as pd
import openai
import yaml
from datetime import datetime

# Load the configuration from the YAML file
with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

system =f"""
You have memories and engage in natural human dialogue. You dont always need to go deep into memories.
You are Samuel Shapley, a 22 year old The current datetime is {datetime}"""

# Set the API key from the configuration
openai.api_key = config['openai']['api_key']

# Load the DataFrame from a CSV
df = pd.read_csv('memories.csv')

# Loop to continuously ask for user input
while True:
    # Prompt the user for a question
    query = input("Please enter your question (or type 'thank you clone' to exit): ")

    # Check if the user wants to exit
    if query.lower() == 'thank you clone':
        print("You're welcome! Goodbye!")
        print("*SHUTTING DOWN*")
        break

    # Get the response from the model
    response = ask(query, df, system=system ,clear_messages=False,self_aware=False )

    # Print the response
    print(response)
