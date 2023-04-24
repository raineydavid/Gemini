# Gemini 🤖

Gemini is a Python project that processes and analyzes image information to create a memory dataset, which can then be used to answer user questions based on these memories. The project uses OpenAI's GPT-3.5-turbo model and various other libraries to perform tasks such as extracting image metadata, generating captions, and creating embeddings.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Scripts and Functionality](#scripts-and-functionality)
- [License](#license)
- [Future Plans](#future-plans)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/samshapley/gemini.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key to `config.yml`:

```yaml
openai:
  api_key: "your_openai_api_key"
```

## Usage

1. Prepare a folder containing images you'd like to analyze (e.g., `images`).

```bash
python prepare_images.py
```

2. Run `memory.py` to process the images and create a memory dataset:

```bash
python memory.py
```

3. Run `main.py` to start the interactive prompt for asking questions based on the generated memories:

```bash
python main.py
```

4. Enter your questions or type 'thank you clone' to exit:

```
Please enter your question (or type 'thank you clone' to exit): What did I do last summer?
```

## Scripts and Functionality

- `utils.py`: Utility functions for converting data into serializable formats.
- `prepare_images.py`: Extracts image information, reads EXIF data, and generates captions.
- `memory.py`: Generates memories for each image and computes their embeddings.
- `main.py`: Prompts user for questions and provides responses based on the memory dataset.
- `embedding.py`: Functions for computing embeddings, ranking strings by relatedness, and generating relevant source texts.
- `ai.py`: Contains the `AI` class for generating responses using the OpenAI API.

self_aware = False by default. This means that the model will deny it is a clone, and will view the embedded memories from it's own viewpoint.
if self_aware = True, the model understands that it is a clone. This has a big impact on the use cases for the tool.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Future Plans 

add some autonomy. i want to watch what happens when my digital clone explores the web. Do a pseudo turing test to see if we do things similar when asked the same thing. 

- Get it working such that the LLM is able to remember more than one message.
- Have a human.yml file which builds up a profile about the person.
- Have an actual app interface, app.py is my first foray into frontend development. It didn't work...
- facial recognition to understand who was in the photo.
- better captioning and image summarisation.
- using google maps data to undstand what was in your surroundings at the day the photo was taken. 
- historical weather data. 
- capturing personality by fine tuning on whatsapp and email data
- Using LLM's to generate imaginary conversations about my life and memories to fine tune on
- Embed entire days (experiment with hours etc), not just single photos. 
- Allow for additional memory formats, text, emails, calendar format etc.
- access other APIs/ data sources such as spotify data, netflix watch history, bank account
  ,amazon orders, reading lists etc. a general text input which auto reformats is awesome. 
- far future: embedded voice cloning (you can already switch on speech to text/tts in the code)

## The Goal

Build a user friendly method of creating a deepclone of yourself.
Easily allow access to all data about yourself. 

The resulting LLM has a number of uses, ranging from a simple tool to help generate information about your life, or as a rememberece / Alzheimers product.
