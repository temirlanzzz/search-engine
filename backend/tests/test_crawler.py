"""The historical live-web crawler test is opt-in, not a unit test."""
import os
import pytest

@pytest.mark.skipif(os.environ.get('RUN_CRAWLER_INTEGRATION') != '1', reason='Requires an explicitly configured database and live network')
def test_crawler():
    from app.crawler.crawler import SimpleCrawler
    crawler = SimpleCrawler(['https://web-scraping.dev'], max_pages=5, delay=1)
    crawler.crawl_and_store()
    assert len(crawler.visited) == 5
