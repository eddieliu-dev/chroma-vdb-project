# This file is configuration of the embedding model.
# 此文件是embedding模型的基础配置 用doubao方式调用

from langchain_ollama import OllamaEmbeddings, ChatOllama

# langchain_llm = ChatOllama(base_url="http://127.0.0.1:11434",
#                            model="bge-m3",
#                            temperature=0.4,
#                            num_ctx=4096)

langchain_embed_model = OllamaEmbeddings(model="bge-m3")