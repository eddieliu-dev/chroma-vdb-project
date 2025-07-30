# This file configures the chroma database cloud client.
# Including: API_KEY, tenant and database name.
# 此文件为chroma db云服务的基础配置 改本地

import chromadb

client = chromadb.CloudClient(
    api_key='ck-HdWFV3R2VLngyLL8NQ3dpf4FCzUu65DJxs71YgVAuYGU',
    tenant='57dca400-ce03-4b94-849c-87be7cb2a8b0',
    database='Test'
)