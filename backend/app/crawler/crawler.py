import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Base folder to save docs
DATA_DIR = "../../../data/docs"
os.makedirs(DATA_DIR, exist_ok=True)

class SimpleCrawler:
    def __init__(self, seed_urls, max_pages=50, delay=1):
        self.visited = set()
        self.to_visit = list(seed_urls)
        self.max_pages = max_pages
        self.delay = delay

    def crawl(self):
        count = 0
        while self.to_visit and count < self.max_pages:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue

            try:
                print(f"Crawling: {url}")
                response = requests.get(url, timeout=5)
                if "text/html" not in response.headers.get("Content-Type", ""):
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.title.string if soup.title else "No Title"
                text = soup.get_text(separator=" ", strip=True)
                links = [urljoin(url, a.get("href")) for a in soup.find_all("a", href=True)]
                links = self._filter_links(links, url)

                self._save_doc(count, url, title, text)
                self.to_visit.extend(links)
                self.visited.add(url)
                count += 1
                time.sleep(self.delay)

            except Exception as e:
                print(f"Failed to crawl {url}: {e}")

    def _save_doc(self, doc_id, url, title, text):
        doc = {
            "id": doc_id,
            "url": url,
            "title": title,
            "text": text,
        }
        with open(os.path.join(DATA_DIR, f"{doc_id}.json"), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)

    def _filter_links(self, links, base_url):
        base_domain = urlparse(base_url).netloc
        filtered = []
        for link in links:
            parsed = urlparse(link)
            if parsed.scheme in ["http", "https"] and parsed.netloc == base_domain:
                filtered.append(link)
        return list(set(filtered))

if __name__ == "__main__":
    seed_urls = ["https://web-scraping.dev"]
    crawler = SimpleCrawler(seed_urls, max_pages=5, delay=1)
    crawler.crawl()
