"""
Crawl TARUMT domains and save discovered URLs to a text file.

Usage:
    python crawl.py              # full crawl, saves tarumt_urls.txt
    python crawl.py --check      # shallow scan (depth 2) to preview external domains
"""

import argparse
from collections import defaultdict
from urllib.parse import urlparse

from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

from config import BASES, URLS_FILE

ALLOWED_DOMAINS = [urlparse(b).netloc for b in BASES]


def crawl(max_depth: int = 99) -> set[str]:
    all_urls: set[str] = set()
    for base in BASES:
        print(f"\nScanning {base}...")
        loader = RecursiveUrlLoader(
            url=base,
            max_depth=max_depth,
            extractor=lambda html: " ",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        docs = loader.load()
        print(f"  Found {len(docs)} URLs")
        for doc in docs:
            all_urls.add(doc.metadata["source"])
    return all_urls


def report_external(urls: set[str]) -> None:
    external: defaultdict[str, list[str]] = defaultdict(list)
    for url in urls:
        domain = urlparse(url).netloc
        if not any(allowed in domain for allowed in ALLOWED_DOMAINS):
            external[domain].append(url)
    print(f"\nExternal domains found: {len(external)}")
    for domain, domain_urls in external.items():
        print(f"\n  {domain} ({len(domain_urls)})")
        for u in domain_urls:
            print(f"    {u}")


def save_urls(urls: set[str], path: str = URLS_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")
    print(f"\nSaved {len(urls)} URLs to {path}")


def load_urls(path: str = URLS_FILE) -> set[str]:
    with open(path, encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Shallow scan to preview external domains")
    args = parser.parse_args()

    if args.check:
        urls = crawl(max_depth=2)
        report_external(urls)
    else:
        urls = crawl(max_depth=99)
        save_urls(urls)
        print(f"\nTotal unique URLs: {len(urls)}")
