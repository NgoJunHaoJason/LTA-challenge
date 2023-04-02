from .prompt_engineering import construct_prompt
from .use_openai import create_embedding, do_chat_completion


SYSTEM_ROLE = "system"
SYSTEM_CONTENT = (
    "You are a helpful assistant representing"
    " the Land Transport Authority of Singapore (LTA)."
)
ASSISTANT_INITIAL_MESSAGE = (
    "GPT: Hi, how can I help you regarding LTA? (Enter 'Quit' to stop)"
)
USER_ROLE = "user"


def run_chat_session_with_lta_info(
    article_embedding_map: dict[str, list[float]],
    verbose: bool = False,
):
    messages = [{"role": SYSTEM_ROLE, "content": SYSTEM_CONTENT}]

    print(ASSISTANT_INITIAL_MESSAGE)
    user_query = input("You: ")

    while user_query != "Quit":
        query_embedding = create_embedding(user_query)
        prompt = construct_prompt(
            user_query,
            query_embedding,
            article_embedding_map,
            verbose,
        )

        messages.append({"role": USER_ROLE, "content": prompt})

        if verbose:
            print(f"prompt:\n{prompt}")

        assistant_message = do_chat_completion(messages)
        messages.append(assistant_message)

        message_content = assistant_message["content"]
        print(f"GPT: {message_content}")

        user_query = input("You: ")


def run_chat_session_without_lta_info():
    messages = [{"role": SYSTEM_ROLE, "content": SYSTEM_CONTENT}]

    print(ASSISTANT_INITIAL_MESSAGE)
    user_query = input("You: ")

    while user_query != "Quit":
        messages.append({"role": USER_ROLE, "content": user_query})

        assistant_message = do_chat_completion(messages)
        messages.append(assistant_message)

        message_content = assistant_message["content"]
        print(f"GPT: {message_content}")

        user_query = input("You: ")
