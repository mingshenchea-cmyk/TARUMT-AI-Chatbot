"""
Entry point: runs the full pipeline or individual steps.

Usage:
    python main.py ingest        # scrape + chunk + embed (run once)
    python main.py chat          # start interactive chatbot
    python main.py crawl         # full URL crawl → tarumt_urls.txt
    python main.py crawl --check # shallow scan to preview external domains
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="TARUMT AI Chatbot")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("ingest", help="Scrape, chunk and embed into ChromaDB")

    chat_p = sub.add_parser("chat", help="Start interactive chatbot")

    crawl_p = sub.add_parser("crawl", help="Crawl TARUMT domains")
    crawl_p.add_argument("--check", action="store_true", help="Shallow scan for external domains")

    args = parser.parse_args()

    if args.cmd == "ingest":
        from ingest import build_vectorstore
        build_vectorstore()

    elif args.cmd == "chat":
        # Import here so model loading only happens for chat
        from chat import build_retriever, chat as ask
        from ingest import load_vectorstore
        from sentence_transformers import CrossEncoder
        from config import RERANK_MODEL

        print("Loading vectorstore...")
        vectorstore, chunks = load_vectorstore()
        retriever = build_retriever(vectorstore, chunks)
        reranker = CrossEncoder(RERANK_MODEL)
        print("Ready. Type your question (Ctrl+C to quit).\n")

        while True:
            try:
                question = input("You: ").strip()
                if not question:
                    continue
                answer = ask(question, retriever, reranker)
                print(f"\nBot: {answer}\n")
            except KeyboardInterrupt:
                print("\nBye!")
                break

    elif args.cmd == "crawl":
        from crawl import crawl, report_external, save_urls
        urls = crawl(max_depth=2 if args.check else 99)
        if args.check:
            report_external(urls)
        else:
            save_urls(urls)
            print(f"Total unique URLs: {len(urls)}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
