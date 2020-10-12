import json
import os
from time import sleep, time

from requests import HTTPError
from tqdm import tqdm

from conf import ua, session, BASE_SEARCH_QUERY_DATA_PATH

REASONABLE_WAITING_TIME = 1  # Seconds

CURRENT_DATA_PATH = BASE_SEARCH_QUERY_DATA_PATH / f"query_hit_{int(time())}.json"


def _get_article_hits_from_query_response(response: dict):
    return response["displaySearchResults"]


def _crawl_pages(*, start_page: int, end_page: int, url: str):
    for page in tqdm(range(start_page, end_page + 1)):
        try:
            r = session.get(f"{url}&page={page}", headers={'user-agent': ua.random})
            r.raise_for_status()
            yield _get_article_hits_from_query_response(r.json())
        except HTTPError:
            print(f"Exception at {page} of page {end_page}")

        sleep(REASONABLE_WAITING_TIME)


def _get_start_end_pages(response: dict):
    _page_meta_data = response["pagingInfo"]
    return _page_meta_data.get("currentPageIndex"), _page_meta_data.get("totalPages")


def _store_query_data(data):
    with open(CURRENT_DATA_PATH, "w+") as out_file:
        json.dump(data, out_file)


def crawl_paginated_search_hits(url: str):
    r = session.get(url, headers={'user-agent': ua.random})
    r.raise_for_status()

    data = r.json()

    start_page, total_pages = _get_start_end_pages(data)

    paginated_query_hits = list(_crawl_pages(start_page=start_page, end_page=total_pages, url=url))
    flattened_query_hits = [items for page in paginated_query_hits for items in page]

    _store_query_data(flattened_query_hits)


if __name__ == '__main__':
    # Example query
    base_url = "https://www.finn.no/api/search?vertical=realestate&subvertical=homes&extension=&appsmarkethint=realestate" \
               "&area_from=45" \
               "&area_to=200" \
               "&no_of_bedrooms_from=1" \
               "&polylocation=10.68141+59.93805%2C10.68674+59.91767%2C10.72450+59.90128%2C10.77035+59.88251%2C10.79151+59.88604%2C10.81566+59.89362%2C10.83068+59.91199%2C10.82067+59.93006%2C10.79929+59.96322%2C10.73546+59.96258%2C10.68141+59.93805" \
               "&price_from=3500000" \
               "&price_to=5700000" \
               "&stored-id=43767246" \
               "&sort=1"

    crawl_paginated_search_hits(base_url)
