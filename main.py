import os

from argparse import ArgumentParser, Namespace
from dotenv import load_dotenv
from typing import cast

from src import (
    create_embedding,
    retrieve_all_saved_news,
    run_chat_session_with_lta_info,
    run_chat_session_without_lta_info,
    save_news,
    setup_openai_api,
    scrape_lta_news,
    DATA_DIR_PATH,
    News,
)


def main():
    if not os.path.exists(".env"):
        print("The .env file that contains OpenAPI's API key is missing.")
        quit(1)

    print("Loading...")

    load_dotenv()
    setup_openai_api()

    args = parse_args()
    no_lta = args.nolta

    if no_lta:
        run_chat_session_without_lta_info()
    else:
        verbose = args.verbose

        os.makedirs(DATA_DIR_PATH, exist_ok=True)
        existing_news_file_names = set(os.listdir(DATA_DIR_PATH))

        try:
            scrape_lta_news(existing_news_file_names, handle_news, verbose)
        except Exception as error:
            print("failed to scrape LTA news due to", error)

        all_news = retrieve_all_saved_news()

        article_embedding_map = {
            news["article"]: news["embedding"] for news in all_news
        }

        run_chat_session_with_lta_info(article_embedding_map, verbose)


def parse_args() -> Namespace:
    arg_parser = ArgumentParser("GPT with latest LTA information")

    arg_parser.add_argument(
        "--nolta",
        action="store_true",
        help="Don't incorporate latest LTA information",
    )
    arg_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Prints more info (helps with debugging)",
    )

    return arg_parser.parse_args()


def handle_news(news: dict):
    embedding = create_embedding(news["article"])
    news["embedding"] = embedding

    news_to_save = cast(News, news)
    save_news(news_to_save, news["file_name"])


if __name__ == "__main__":
    main()
