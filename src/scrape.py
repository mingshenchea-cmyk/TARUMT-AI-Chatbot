"""
Scrape and clean page content from the main TARUMT site.

Usage:
    python scrape.py             # scrapes https://www.tarc.edu.my, returns docs
    python scrape.py --verbose   # also prints each page's URL
"""

import argparse
import re

from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_core.documents import Document

BASE = "https://www.tarc.edu.my"

JUNK_PATTERNS = [
    ".css",
    "flang=BM",
    "news_archive.jsp?cat_id=",
]


def clean_text(html: str) -> str:
    soup = Soup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def is_valid_url(url: str) -> bool:
    return not any(p in url for p in JUNK_PATTERNS)


def scrape() -> list[Document]:
    loader = RecursiveUrlLoader(
        url=f"{BASE}/",
        max_depth=99,
        extractor=clean_text,
        exclude_dirs=[f"{BASE}/assets"],
        headers={"User-Agent": "Mozilla/5.0"},
    )
    docs = loader.load()
    docs = [doc for doc in docs if is_valid_url(doc.metadata["source"])]
    return docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    docs = scrape()
    print(f"Clean pages scraped: {len(docs)}")
    if args.verbose:
        for doc in docs:
            print(f"  {doc.metadata['source']}")
