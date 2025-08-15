# Chroma VDB + LLM Document Processing

This project combines a local **Chroma vector database** with a **local LLM API (via Ollama)** to process and query text documents. It performs document embedding, title and keyword extraction, and supports semantic search via natural language queries.

---

## 🚀 Features

- **Add Mode**:  
  - Creates a Chroma collection if it does not exist  
  - Reads documents from a local file  
  - Generates vector embeddings for each document using `langchain` with the `bge-m3` model  
  - Uses an LLM to:
    - Generate a concise title (≤10 characters)
    - Extract 3–5 relevant keywords  
  - Generates additional metadata:
    - Unique document ID
    - Random creator name
    - Random creation timestamp  
  - Stores the document, embedding, and metadata in the Chroma database  
- **Query Mode**:  
  - Searches the Chroma database using vector similarity  
  - Returns document content and metadata including title and keywords

---

## 📂 Project Structure

```
chroma-vdb-project/
│
├── chroma/                     # Chroma DB setup and operations
│   ├── chroma_client.py        # Initializes Chroma DB client
│   └── chroma_function.py      # CRUD operations for Chroma
│
├── chroma_data/                # Persistent storage for Chroma
│
├── data/                       # Raw input documents
│   ├── documents_dup_part_1_part_1
│   └── documents_dup_part_1_part_1_short
│
├── helpers/                    # General-purpose helpers
│   ├── prompt.py               # Prompt templates for LLM
│   └── record_helper.py        # Metadata and document ID utilities
│
├── llm/                        # LLM API and embedding utilities
│   ├── llm_client.py           # Sends prompt to local LLM (Ollama)
│   └── llm_embedding.py        # Embedding function using Langchain + Ollama
│
├── service/                    # Empty for future improvements
│
├── README.md                   # Project documentation
└── main.py                     # Main entry point
```

---

## ✨ Future Improvements

- [ ] Add multi-language support
- [ ] Add more service features
- [ ] Combine Chroma vdb with Elasticsearch to perform preciser RAG function