import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from app.config import settings
from app.services.document_service import DocumentService
from app.database import SessionLocal
from app.utilts.tokenizer import tokenize_text

def get_website_name(url: str) -> str | None:
    try:
        # Ensure the URL has a scheme so urlparse works correctly
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        parsed = urlparse(url)
        hostname = parsed.hostname or ''
        
        # Strip "www." if present
        return hostname.removeprefix('www.')
    except Exception as e:
        print(f"Invalid URL: {url} — {e}")
        return None

class SimpleCrawler:
    def __init__(self, seed_urls, max_pages=50, delay=1):
        self.visited = set()
        self.to_visit = list(seed_urls)
        self.max_pages = max_pages
        self.delay = delay
        self.db = SessionLocal()
        self.document_service = DocumentService(self.db)

    def crawl_and_store(self):
        count = 0
        while self.to_visit and count < self.max_pages:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue

            try:
                print(f"Crawling: {url}")
                response = requests.get(url, timeout=5)
                content_type = response.headers.get("Content-Type", "")
                
                title = "No Title"
                text = ""
                links = []
                
                if "text/html" in content_type:
                    # Parse HTML content
                    soup = BeautifulSoup(response.text, "html.parser")
                    title = soup.title.string if soup.title else "No Title"
                    text = soup.get_text(separator=" ", strip=True)
                    links = [urljoin(url, a.get("href")) for a in soup.find_all("a", href=True)]
                    links = self._filter_links(links, url)
                elif "application/json" in content_type:
                    # Parse JSON content
                    try:
                        json_data = response.json()
                        title = f"JSON Response from {get_website_name(url)}"
                        text = json.dumps(json_data, indent=2)
                    except json.JSONDecodeError:
                        title = f"Invalid JSON from {get_website_name(url)}"
                        text = response.text
                else:
                    # Handle other content types as plain text
                    title = f"Content from {get_website_name(url)}"
                    text = response.text

                # Save document to database
                self._save_doc_to_db(url, title, text)
                
                self.to_visit.extend(links)
                self.visited.add(url)
                count += 1
                time.sleep(self.delay)

            except Exception as e:
                print(f"Failed to crawl {url}: {e}")
        
        # Close database session
        self.db.close()

    def _save_doc_to_db(self, url, title, text):
        try:
            # Create document using the correct method signature
            document = self.document_service.create_document(url, title, text)
            print(f"Saved document to database: {title}")
            
        except Exception as e:
            print(f"Failed to save document to database: {e}")

    def _filter_links(self, links, base_url):
        base_domain = urlparse(base_url).netloc
        filtered = []
        for link in links:
            parsed = urlparse(link)
            if parsed.scheme in ["http", "https"] and parsed.netloc == base_domain:
                filtered.append(link)
        return list(set(filtered))

