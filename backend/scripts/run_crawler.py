from app.crawler.crawler import SimpleCrawler

def crawl_and_store(urls, max_pages=10, delay=1):
    crawler = SimpleCrawler(urls, max_pages=max_pages, delay=delay)
    crawler.crawl_and_store()