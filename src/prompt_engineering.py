import numpy as np


PROMPT_HEADER = (
    "Answer the question as truthfully"
    " as possible using the provided context,"
    " and if the answer is not contained within the text below,"
    " ask the questioner to rephrase their question."
)


def construct_prompt(
    user_query: str,
    query_embedding: list[float],
    article_embedding_map: dict[str, list[float]],
    verbose: bool = False,
) -> str:
    article = _find_most_similar_article(
        query_embedding,
        article_embedding_map,
    )

    if verbose:
        print(f"most similar article:\n{article[:30]}...")

    return f"{PROMPT_HEADER}\n\nContext:\n{article}\n\nQuestion: {user_query}"


def _find_most_similar_article(
    query_embedding: list[float],
    article_embedding_map: dict[str, list[float]],
) -> str:
    similarity_scores = {
        article: _get_vector_similarity(query_embedding, article_embedding)
        for article, article_embedding in article_embedding_map.items()
    }

    return max(
        similarity_scores,
        key=similarity_scores.__getitem__,
        default="",
    )


def _get_vector_similarity(
    x: list[float] | np.ndarray,
    y: list[float] | np.ndarray,
) -> float:
    """Returns the similarity between two vectors.

    Because OpenAI Embeddings are normalized to length 1,
    the cosine similarity is the same as the dot product.
    """
    return np.dot(x, y)
