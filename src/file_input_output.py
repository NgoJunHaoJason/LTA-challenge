import orjson
import os

from datetime import datetime
from typing import TypedDict


DATA_DIR_PATH = "data"


News = TypedDict(
    "News",
    {
        "title": str,
        "date": datetime | None,
        "tags": list[str],
        "article": str,
        "file_name": str,
        "embedding": list[float],
    },
)


def retrieve_all_saved_news() -> list[News]:
    return [
        _retrieve_saved_news(os.path.join(DATA_DIR_PATH, file_name))
        for file_name in os.listdir(DATA_DIR_PATH)
    ]


def _retrieve_saved_news(file_path: str) -> News:
    with open(file_path) as file:
        news_json = "\n".join(file.readlines())

    return orjson.loads(news_json)


def save_news(news: News, file_name: str):
    data_file_path = os.path.join(DATA_DIR_PATH, file_name)
    json_string = orjson.dumps(news, option=orjson.OPT_INDENT_2)

    with open(data_file_path, mode="wb") as date_file:
        date_file.write(json_string)
