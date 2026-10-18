"""Create the persistent client only when a database operation is requested."""

from functools import lru_cache

import chromadb

from config import CHROMA_PATH


@lru_cache(maxsize=1)
def get_client():
    return chromadb.PersistentClient(path=str(CHROMA_PATH))
