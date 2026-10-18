# llm_embedding.py
#
# This file configures the embedding model using Langchain's OllamaEmbeddings.
# It uses the "bge-m3:latest" model.
#
# 此文件通过 Langchain 的 OllamaEmbeddings 配置 embedding 模型，
# 使用 "bge-m3:latest" 模型l。

from langchain_ollama import OllamaEmbeddings

from config import EMBEDDING_MODEL, OLLAMA_BASE_URL, OLLAMA_TIMEOUT

langchain_embed_model = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=OLLAMA_BASE_URL,
    client_kwargs={"timeout": OLLAMA_TIMEOUT},
)
