# This file configures the chroma database cloud client.
# Including: API_KEY, tenant and database name.
# 此文件为chroma db云服务的基础配置 改本地

import chromadb

client = chromadb.PersistentClient(path="./chroma_data")