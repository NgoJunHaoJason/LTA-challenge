import requests
import re

from bs4 import BeautifulSoup, Tag
from datetime import datetime
from typing import Callable


LTA_BASE_URL = "https://www.lta.gov.sg"
LTA_NEWSROOM_URL = f"{LTA_BASE_URL}/content/ltagov/en/newsroom.html"

FROM_YEAR = 2021
TO_YEAR = datetime.today().year

PARAGRAPH_NUMBER = re.compile(r"\n\d+\W{3}")


def scrape_lta_news(
    existing_news_file_names: set[str],
    handle_news: Callable[[dict], None],
    verbose: bool = False,
):
    """Crawl LTA's newsroom and save news releases

    Parameters
    ----------
    verbose : bool, optional
        prints information if True, by default False
    """
    response = requests.get(LTA_NEWSROOM_URL)
    html_doc = response.text

    soup = BeautifulSoup(html_doc, features="html.parser")
    links = soup.find_all(name="a")

    link: Tag
    for link in links:
        link_url = str(link["href"])

        if not (_is_news_release_url(link_url)):
            continue

        split_url = link_url.split("/")
        year = int(split_url[5])

        if not (FROM_YEAR <= year <= TO_YEAR):
            continue

        month = split_url[6]
        article_name = split_url[8].replace(".html", "")

        file_name = f"{year}_{month}_{article_name}.json"
        if file_name in existing_news_file_names:
            continue

        news_url = f"{LTA_BASE_URL}{link_url}"
        news = _retrieve_lta_news(news_url)
        news["file_name"] = file_name

        handle_news(news)

        if verbose:
            print(f"done scraping from {link_url}")

    if verbose:
        print("done scraping news releases from LTA")


def _is_news_release_url(url: str) -> bool:
    return url.startswith("/content/ltagov/en/newsroom/")


def _retrieve_lta_news(news_url: str) -> dict:
    response = requests.get(news_url)
    html_doc = response.text

    soup = BeautifulSoup(html_doc, features="html.parser")
    return {
        "title": _get_news_title(soup),
        "date": _get_date(soup),
        "tags": _get_keyword_tags(soup),
        "article": _get_news_article(soup),
    }


def _get_news_title(soup: BeautifulSoup) -> str:
    title = soup.find("h2", class_="page-title")
    return title.get_text() if title else ""


def _get_date(soup: BeautifulSoup) -> datetime | None:
    date = soup.find("span", class_="header-date-tag")
    return datetime.strptime(date.get_text(), "%d %b %Y") if date else None


def _get_keyword_tags(soup: BeautifulSoup) -> list[str]:
    keyword_tags = soup.find_all("a", class_="header-tag keywords")
    return [tag.get_text() for tag in keyword_tags]


def _get_news_article(soup: BeautifulSoup) -> str:
    article_sections = soup.find_all("div", class_="text parbase section")

    return " ".join(
        [
            processed_paragraph
            for section in article_sections
            for paragraph in _extract_paragraphs(section.get_text())
            if (processed_paragraph := paragraph.strip()) != ""
        ]
    )


def _extract_paragraphs(text: str) -> list[str]:
    return re.sub(PARAGRAPH_NUMBER, "\n", text).split("\n")
