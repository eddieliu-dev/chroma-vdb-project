"""Read one UTF-8 document per line and attach reproducible identifiers."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def file_reader(file_name: str | Path) -> list[str]:
    with open(file_name, encoding="utf-8") as source:
        return [line.strip() for line in source if line.strip()]


def document_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate_metadata(title: str, keywords: list[str], source: str) -> dict:
    # JSON text keeps keywords compatible with scalar metadata in Chroma 1.x.
    return {
        "title": title,
        "keywords": json.dumps(keywords, ensure_ascii=False),
        "source": source,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
