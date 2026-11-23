"""
RAG chatbot: BM25 + vector ensemble retriever with cross-encoder reranker.

Usage:
    python chat.py               # interactive loop
"""

import requests
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from sentence_transformers import CrossEncoder

from config import PHI4_API_URL, PHI4_MODEL, RERANK_MODEL
from ingest import load_vectorstore

SYSTEM_PROMPT = (
    "You are a helpful assistant for TARUMT (Tunku Abdul Rahman University of Management and Technology). "
    "Answer using ONLY the provided context. "
    "If the answer is not in the context, say 'I don't have that information.'"
)


def build_retriever(vectorstore, chunks):
    bm25 = BM25Retriever.from_documents(chunks)
    bm25.k = 5
    vector = vectorstore.as_retriever(search_kwargs={"k": 5})
    return EnsembleRetriever(retrievers=[bm25, vector], weights=[0.4, 0.6])


def chat(question: str, retriever, reranker: CrossEncoder) -> str:
    results = retriever.invoke(question)

    pairs = [[question, doc.page_content] for doc in results]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(scores, results), reverse=True)
    top_chunks = [doc for _, doc in ranked[:3]]

    context = "\n\n".join(doc.page_content for doc in top_chunks)

    response = requests.post(
        PHI4_API_URL,
        json={
            "model": PHI4_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
            ],
        },
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
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
            answer = chat(question, retriever, reranker)
            print(f"\nBot: {answer}\n")
        except KeyboardInterrupt:
            print("\nBye!")
            break
