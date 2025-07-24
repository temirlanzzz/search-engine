from app.crawler.crawler import SimpleCrawler

def test_crawler():
    seed_urls = ["https://web-scraping.dev"]
    crawler = SimpleCrawler(seed_urls, max_pages=5, delay=1)
    crawler.crawl_and_store()
    assert len(crawler.visited) == 5