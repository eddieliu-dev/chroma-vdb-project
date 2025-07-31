# This file contains all the chroma function that may potentially be in use.
# Including: create, get, peek, modify and delete collection; count records, etc
# 此文件包含了chroma db运行将会用到的一些方法

from chromadb import GetResult
from chromadb.types import Collection  # Import the Collection type
from datetime import datetime
# noinspection PyUnresolvedReferences
from chroma import chroma_client
from llm import llm_embedding


# If there is not a collection with name "collection_name", create one.
# If there is, get the collection.
# 如果没有叫collection_name的集合-创建；如果有-获取
def create_collection(collection_name, description) -> Collection:
    if collection_name not in chroma_client.client.list_collections(limit=10):
        collection = chroma_client.client.get_or_create_collection(
            name=collection_name,
            # 'OllamaEmbeddings' object has no attribute 'name'
            # embedding_function=embedding_function,
            metadata={
                "description": description,
                "created": str(datetime.now())
            },
            configuration={
                "hnsw": {
                    "space": "cosine",
                    "ef_construction": 100
                }
            }
        )
    else:
        collection = chroma_client.client.get_collection(name=collection_name)
    return collection


# Get the collection. 获取集合
def get_collection(collection_name) -> Collection:
    collection = chroma_client.client.get_collection(name=collection_name)
    return collection


# Returns the first 10 records of the collection. 返回集合中的前10个数据
def peek_collection(collection_name) -> GetResult:
    collection = get_collection(collection_name)
    return collection.peek()

def query_collection(collection_name, query, query_text, results_include, results_number):
    collection = get_collection(collection_name)
    result = collection.query(
        query_embeddings=llm_embedding.langchain_embed_model.embed_query(query),
        query_texts=[query_text],
        include=results_include,
        n_results=results_number
    )
    return result


# Change the name of the collection. 给集合改名
def modify_collection(old_name, new_name):
    collection = get_collection(old_name)
    collection.modify(
        old_name=new_name
    )


# Delete the collection. 删除集合
def delete_collection(collection_name):
    chroma_client.client.delete_collection(name=collection_name)


# Returns the number of records in a collection. 返回集合中数据的个数
def count_record(collection_name) -> int:
    collection = get_collection(collection_name)
    return collection.count()


# Add data to a collection. 给指定合集添加数据
def add_data(collection_name, ids,embeddings, documents, metadatas):
    collection = get_collection(collection_name)
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


# Update data in a collection. 更改指定集合数据
def update_data(collection_name, ids, documents, metadatas):
    collection = get_collection(collection_name)
    collection.update(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )


# Delete data in a collection. 删除指定合集数据
def delete_data(collection_name, ids, where):
    collection = get_collection(collection_name)
    if where is None:
        collection.delete(
            ids=ids
        )
    elif ids is None:
        collection.delete(
            where=where
        )
    else:
        collection.delete(
            ids=ids,
            where=where
        )
