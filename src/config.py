"""Shared constants used across all modules."""

import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASES = [
    "https://www.tarc.edu.my",
    "https://sabah.tarc.edu.my",
    "https://focs.tarc.edu.my",
    "https://fssh.tarc.edu.my",
    "https://fobe.tarc.edu.my",
    "https://sme.tarc.edu.my",
    "https://fafb.tarc.edu.my",
    "https://pahang.tarc.edu.my",
    "https://spacerent.tarc.edu.my",
    "https://cpsr.tarc.edu.my",
    "https://fcci.tarc.edu.my",
    "https://portal.tarc.edu.my",
    "https://cbiev.tarc.edu.my",
    "https://library.tarc.edu.my",
    "https://penang.tarc.edu.my",
    "https://sites.tarc.edu.my",
    "https://foet.tarc.edu.my",
    "https://examination.tarc.edu.my",
    "https://sustainability.tarc.edu.my",
    "https://web.tarc.edu.my",
    "https://johor.tarc.edu.my",
    "https://perak.tarc.edu.my",
    "https://foas.tarc.edu.my",
    "https://cpus.tarc.edu.my",
    "https://iser.tarc.edu.my",
]

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
CHROMA_DIR = os.path.join(_PROJECT_ROOT, "tarumt_db")
CHROMA_COLLECTION = "tarumt"
URLS_FILE = os.path.join(_PROJECT_ROOT, "tarumt_urls.txt")

PHI4_API_URL = "http://192.168.90.132:31419/v1/chat/completions"
PHI4_MODEL = "microsoft/Phi-4-multimodal-instruct"
