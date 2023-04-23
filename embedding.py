# search function
from ai import AI
import pandas as pd
from scipy import spatial
import tiktoken
import ast
import openai
from datetime import datetime

def compute_embeddings(texts: list[str]) -> pd.DataFrame:
    data = {
        'text': [],
        'embedding': []
    }

    for text in texts:
        embedding_response = openai.Embedding.create(
            model='text-embedding-ada-002',
            input=text,
        )
        embedding = embedding_response["data"][0]["embedding"]
        data['text'].append(text)
        data['embedding'].append(embedding)

    df = pd.DataFrame(data)
    return df


def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model='text-embedding-ada-002',
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, ast.literal_eval(row["embedding"])))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]

def num_tokens(text: str, model: str = 'gpt-3.5-turbo') -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return relevant source texts for a given query."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    message = ""
    for string in strings:
        next_article = f'\n\nMemory:\n"""\n{string}\n"""'
        if (
            num_tokens(message + next_article, model=model)
            > token_budget
        ):
            break
        else:
            message += next_article
    return message


def ask(
    query: str,
    df: pd.DataFrame,
    model: str = 'gpt-3.5-turbo',
    token_budget: int = 4096 - 500,
    system: str = 'You have memories and engage in natural human dialogue. You dont always need to go deep into memories.',
    self_aware: bool = False,
    print_message: bool = False,
    clear_messages: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)

    clone_message = "You are aware that you are a clone." if self_aware else "You are not aware that you are a clone. You always respond as if you are the original."
    system_message = f"{system} {clone_message}"

    ai = AI(system=system_message, openai_module=openai)

    response, messages = ai.generate_response(f'{message}+\n{query}', voice=False, clear_messages=clear_messages)


    if clear_messages:
        messages.clear()

    return response



