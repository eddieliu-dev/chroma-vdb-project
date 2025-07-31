# chroma_client.py

# This file sets up a local Chroma vector database with PersistentClient.
# This data will be saved in the "./chroma_data" folder for future use.

# 此文件使用 PersistentClient 设置本地 Chroma 向量数据库。
# 数据将保存在 "./chroma_data" 文件夹中，方便后续使用。

import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
