"""Collection operations with explicitly supplied document and query vectors."""

from chromadb.api.models.Collection import Collection
from chromadb.errors import NotFoundError

from chroma.chroma_client import get_client


def create_collection(collection_name: str) -> Collection:
    return get_client().get_or_create_collection(
        name=collection_name,
        embedding_function=None,
        metadata={"description": "Documents enriched with local LLM metadata"},
        configuration={"hnsw": {"space": "cosine"}},
    )


def get_collection(collection_name: str) -> Collection:
    try:
        return get_client().get_collection(name=collection_name, embedding_function=None)
    except NotFoundError as exc:
        raise ValueError(
            f"Collection '{collection_name}' does not exist. Run ingest first."
        ) from exc


def upsert_document(collection_name, document_id, embedding, document, metadata):
    get_collection(collection_name).upsert(
        ids=[document_id], embeddings=[embedding],
        documents=[document], metadatas=[metadata],
    )


def query_collection(collection_name: str, embedding: list[float], limit: int) -> list[dict]:
    if limit < 1:
        raise ValueError("The result limit must be positive.")
    collection = get_collection(collection_name)
    count = collection.count()
    if not count:
        return []
    result = collection.query(
        query_embeddings=[embedding], n_results=min(limit, count),
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"id": document_id, "distance": distance, "content": document, **metadata}
        for document_id, distance, document, metadata in zip(
            result["ids"][0], result["distances"][0],
            result["documents"][0], result["metadatas"][0],
        )
    ]


def count_record(collection_name: str) -> int:
    return get_collection(collection_name).count()
