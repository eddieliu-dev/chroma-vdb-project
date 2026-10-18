"""Local configuration; environment variables override the optional .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "300"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "bge-m3:latest")
CHROMA_PATH = Path(os.getenv("CHROMA_PATH", "chroma_data")).expanduser()
if not CHROMA_PATH.is_absolute():
    CHROMA_PATH = ROOT / CHROMA_PATH
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "documents")
