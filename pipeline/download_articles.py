import json
import os
import re
from operator import itemgetter
from pathlib import Path
from time import sleep

from requests import HTTPError
from tqdm import tqdm

from conf import BASE_DATA_PATH, session, ua, BASE_SEARCH_QUERY_DATA_PATH
from pipeline.types import ArticlePreScraping

BASE_ARTICLE_DATA_PATH = BASE_DATA_PATH / "raw_articles"
REASONABLE_WAITING_TIME = 1  # Seconds


def _download_article(article: ArticlePreScraping):
    url = article.full_url
    r = session.get(url, headers={'user-agent': ua.random})

    try:
        r.raise_for_status()
    except HTTPError:
        return

    html = r.html

    data_path = BASE_ARTICLE_DATA_PATH / Path(article.id)

    if not data_path.exists():
        os.makedirs(data_path)

    with open(data_path / "source.html", "w+") as out_file:
        out_file.write(html.raw_html.decode("utf-8"))


def download_articles():
    files_in_query_data_path = BASE_SEARCH_QUERY_DATA_PATH.iterdir()
    query_hit_files = (file for file in files_in_query_data_path if
                       file.is_file() and file.name.startswith("query_hit"))

    def _get_time_from_filename(file: Path):
        match, *_ = re.search("query_hit_([0-9].*).json", file.name).groups()
        return int(match)

    files_with_times = ((file, _get_time_from_filename(file)) for file in query_hit_files)

    newest_file, _ = max(files_with_times, key=itemgetter(1))

    with open(newest_file, "r+") as in_file:
        articles_to_scrape = json.load(in_file)

    for raw_article in tqdm(articles_to_scrape):
        article = ArticlePreScraping(url=raw_article.get("adUrl"))
        _download_article(article=article)
        sleep(REASONABLE_WAITING_TIME)


if __name__ == '__main__':
    download_articles()
