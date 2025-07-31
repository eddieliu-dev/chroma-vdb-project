# Chroma VDB + LLM Document Processing

This project combines a local **Chroma vector database** with a **local LLM API (via Ollama)** to process and query text documents. It performs document embedding, title and keyword extraction, and supports semantic search via natural language queries.

---

## 📂 Project Structure

```
chroma-vdb-project/
│
├── chroma/                     # Chroma DB setup and operations
│   ├── __init__.py
│   ├── chroma_client.py        # Initializes Chroma DB client
│   └── chroma_function.py      # CRUD operations for Chroma
│
├── chroma_data/                # Persistent storage for Chroma
│
├── data/                       # Raw input documents
│   ├── documents_dup_part_1_part_1
│   └── documents_dup_part_1_part_1_short
│
├── llm/                        # LLM API and embedding utilities
│   ├── __init__.py
│   ├── llm_client.py           # Sends prompt to local LLM (Ollama)
│   └── llm_embedding.py        # Embedding function using Langchain + Ollama
│
├── service/                    # Empty for future improvements
│
├── main.py                     # Main entry point
├── prompt.py                   # Prompt templates for LLM
├── record_helper.py            # Metadata and document ID utilities
├── README.md                   # Project documentation
└── .venv/                      # Virtual environment (excluded from Git)
```

---

## 🚀 Features

- ✅ Extracts embeddings from raw text using `bge-m3` model
- 🧠 Uses a local LLM (`llama3.1:latest`) to extract:
  - 🔹 Short titles
  - 🔹 3–5 keywords
- 🗃️ Stores data in Chroma with metadata (UUID, creator, timestamp)
- 🔍 Supports semantic search based on user query

---

## 🛠️ Setup

1. **Install dependencies**  
   Use `poetry` or `pip` to install:
   ```bash
   pip install chromadb langchain aiohttp
   ```

2. **Start Ollama LLM Server**  
   Install and start Ollama:
   ```bash
   ollama run llama3
   ```

3. **Run the project**
   ```bash
   python main.py
   ```

---

## 📘 How It Works

- When you run `main.py`, you can choose:
  - `Add`: reads text, generates embeddings, metadata, stores in Chroma
  - `Query`: asks a semantic question, returns best-matching document

- The prompts used:
  - Title prompt: generates a short (≤10 characters) summary
  - Keywords prompt: extracts 3–5 topic-relevant keywords

---

## 📄 Example Query

```text
有没有美国相关的新闻?
```

Returns:
- Matched title  
- Extracted keywords  
- Full document text

---

## ✨ Future Improvements

- [ ] Add multi-language support
- [ ] Add more service features