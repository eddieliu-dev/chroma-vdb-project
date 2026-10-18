"""Exercise real Chroma persistence using tiny explicit vectors, with no model calls."""

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import chromadb

import main
from chroma import chroma_function as db
from helpers.record_helper import generate_metadata


class ChromaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.client = chromadb.PersistentClient(path=cls.directory.name)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def setUp(self):
        self.patcher = patch("chroma.chroma_function.get_client", return_value=self.client)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_upsert_preserves_other_documents_and_search_ranks_all_hits(self):
        name = "ranked-search"
        db.create_collection(name)
        metadata = generate_metadata("Solar", ["sun", "roof", "power"], "test.txt")
        db.upsert_document(name, "solar", [1.0, 0.0], "Solar power", metadata)
        db.upsert_document(name, "rail", [0.0, 1.0], "Rail transport", metadata)
        db.upsert_document(name, "solar", [1.0, 0.0], "Updated solar power", metadata)
        db.create_collection(name)
        self.assertEqual(db.count_record(name), 2)
        results = db.query_collection(name, [1.0, 0.0], limit=10)
        self.assertEqual([result["id"] for result in results], ["solar", "rail"])
        self.assertEqual(results[0]["content"], "Updated solar power")
        self.assertLess(results[0]["distance"], results[1]["distance"])

    def test_empty_collection_returns_empty_results(self):
        db.create_collection("empty-search")
        self.assertEqual(db.query_collection("empty-search", [1.0, 0.0], 3), [])

    def test_missing_collection_explains_ingestion(self):
        with self.assertRaisesRegex(ValueError, "Run ingest first"):
            db.count_record("missing-search")

    def test_ingestion_embeds_whole_documents_and_reruns_without_duplicates(self):
        metadata = {"title": "Solar", "keywords": ["sun", "roof", "power"]}
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.txt"
            source.write_text("Solar power\nRail transport\n", encoding="utf-8")
            with patch("main.llm_client.extract_metadata", new=AsyncMock(return_value=metadata)), \
                 patch("main.llm_embedding.langchain_embed_model") as model:
                embed = model.aembed_documents = AsyncMock(return_value=[[1.0, 0.0]])
                for _ in range(2):
                    self.assertEqual(asyncio.run(main.ingest_documents(str(source), "ingestion")), 2)
                self.assertEqual(embed.call_args_list[0].args[0], ["Solar power"])
                self.assertEqual(embed.call_args_list[1].args[0], ["Rail transport"])
        results = main.run(main.build_parser().parse_args(["count", "--collection", "ingestion"]))
        self.assertEqual(results["count"], 2)

    def test_query_passes_user_text_and_decodes_keywords(self):
        db.create_collection("cli-query")
        db.upsert_document("cli-query", "solar", [1.0, 0.0], "Solar power",
                           generate_metadata("Solar", ["sun", "roof", "power"], "sample.txt"))
        with patch("main.llm_embedding.langchain_embed_model") as model:
            embed = model.embed_query
            embed.return_value = [1.0, 0.0]
            results = main.run(main.build_parser().parse_args([
                "query", "clean electricity", "--collection", "cli-query", "--limit", "1"
            ]))
        embed.assert_called_once_with("clean electricity")
        self.assertEqual(results[0]["keywords"], ["sun", "roof", "power"])
        json.dumps(results)
