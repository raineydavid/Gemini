# Gemini

Gemini is a Python project that processes and analyzes image information to create a memory dataset, which can then be used to answer user questions based on these memories. The project uses OpenAI's GPT-3.5-turbo model and various other libraries to perform tasks such as extracting image metadata, generating captions, and creating embeddings.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Scripts and Functionality](#scripts-and-functionality)
- [License](#license)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gemini.git
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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
