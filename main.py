"""Ingest documents and run semantic searches against local Chroma storage."""

import argparse
import asyncio
import json
import sys

import aiohttp
import httpx
from chromadb.errors import ChromaError
from ollama import ResponseError

from chroma import chroma_function
from config import CHROMA_COLLECTION, OLLAMA_TIMEOUT, ROOT
from helpers import record_helper
from llm import llm_client, llm_embedding


def positive_int(value: str) -> int:
    result = int(value)
    if result < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest", help="Enrich and upsert one document per line")
    ingest.add_argument("--file", default=str(ROOT / "data/sample.txt"))
    query = commands.add_parser("query", help="Search documents by meaning")
    query.add_argument("text", help="Natural-language search query")
    query.add_argument("--limit", type=positive_int, default=3)
    count = commands.add_parser("count", help="Count stored documents")
    for command in (ingest, query, count):
        command.add_argument("--collection", default=CHROMA_COLLECTION)
    return parser


async def ingest_documents(file_name: str, collection_name: str) -> int:
    documents = record_helper.file_reader(file_name)
    if not documents:
        raise ValueError("The input file contains no documents.")
    chroma_function.create_collection(collection_name)
    timeout = aiohttp.ClientTimeout(total=OLLAMA_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for number, document in enumerate(documents, start=1):
            metadata = await llm_client.extract_metadata(document, session)
            # Pass a list of documents, not a string of characters.
            embeddings = await llm_embedding.langchain_embed_model.aembed_documents([document])
            chroma_function.upsert_document(
                collection_name, record_helper.document_id(document), embeddings[0], document,
                record_helper.generate_metadata(**metadata, source=str(file_name)),
            )
            print(f"[{number}/{len(documents)}] {metadata['title']}", file=sys.stderr)
    return chroma_function.count_record(collection_name)


def run(args: argparse.Namespace):
    if args.command == "ingest":
        return {"collection": args.collection, "count": asyncio.run(
            ingest_documents(args.file, args.collection)
        )}
    if args.command == "count":
        return {"collection": args.collection, "count": chroma_function.count_record(args.collection)}
    if not args.text.strip():
        raise ValueError("The search query must not be blank.")
    if not chroma_function.count_record(args.collection):
        return []
    embedding = llm_embedding.langchain_embed_model.embed_query(args.text)
    results = chroma_function.query_collection(args.collection, embedding, args.limit)
    for result in results:
        result["keywords"] = json.loads(result["keywords"])
    return results


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = run(args)
    except (OSError, ValueError, RuntimeError, httpx.HTTPError, ChromaError, ResponseError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
