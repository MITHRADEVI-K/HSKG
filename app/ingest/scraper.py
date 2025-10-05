"""Web scraping utilities (placeholder).

For production you might accept a list of URLs and return raw HTML content
cleaned with BeautifulSoup. This stub is here so higher-level code can call
`fetch_reviews()` without failing.
"""

from __future__ import annotations

from typing import List

import requests
from bs4 import BeautifulSoup


def fetch_reviews(urls: List[str]) -> List[str]:
    """Fetch review texts from the provided URLs (very naive implementation)."""
    texts: list[str] = []
    for url in urls:
        try:
            html = requests.get(url, timeout=10).text
            soup = BeautifulSoup(html, "html.parser")
            # collect all paragraph text as example
            texts.extend(p.get_text(" ", strip=True) for p in soup.find_all("p"))
        except Exception as exc:  # pragma: no cover – simple demo
            print(f"[scraper] failed {url}: {exc}")
    return texts
