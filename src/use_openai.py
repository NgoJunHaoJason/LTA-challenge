import openai
import os

EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_COMPLETION_MODEL = "gpt-3.5-turbo"

TEMPERATURE = 0.0  # for the most predictable, factual answer


def setup_openai_api():
    openai.api_key = os.getenv("OPENAI_API_KEY")


def create_embedding(text: str) -> list[float]:
    """Call OpenAI's API to create an embedding for a given text.

    Parameters
    ----------
    text : str
        text to be represented as embedding

    Returns
    -------
    list[float]
        embedding
    """
    result = openai.Embedding.create(model=EMBEDDING_MODEL, input=text)
    return result["data"][0]["embedding"]


def do_chat_completion(messages: list[dict[str, str]]) -> dict[str, str]:
    """Call OpenAI's API for chat completion.

    Parameters
    ----------
    messages : list[dict[str, str]]
        [{"role": "some_role", "content": "some_content"}]

    Returns
    -------
    dict[str, str]
        {"role": "assistant", "content": "reply_from_gpt"}
    """
    response: dict = openai.ChatCompletion.create(
        messages=messages,
        model=CHAT_COMPLETION_MODEL,
        temperature=TEMPERATURE,
    )
    return response["choices"][0]["message"]
