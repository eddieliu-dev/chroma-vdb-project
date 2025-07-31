# llm_embedding.py
#
# This file configures the embedding model using Langchain's OllamaEmbeddings.
# It uses the "bge-m3:latest" model.
#
# 此文件通过 Langchain 的 OllamaEmbeddings 配置 embedding 模型，
# 使用 "bge-m3:latest" 模型。

from langchain_ollama import OllamaEmbeddings

langchain_embed_model = OllamaEmbeddings(model="bge-m3:latest")
