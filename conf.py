from pathlib import Path

from fake_useragent import UserAgent
from requests_html import HTMLSession

BASE_DATA_PATH = Path("./data")
BASE_SEARCH_QUERY_DATA_PATH = BASE_DATA_PATH / "query_hits"

session = HTMLSession(mock_browser=True)
ua = UserAgent()
