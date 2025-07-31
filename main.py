# This is the main file of the project. 此文件是项目的主文件
# All the operations will eventually run here

import asyncio
from chroma import chroma_client, chroma_function
from llm import llm_embedding, llm_provider
import document_parser, prompt, text_prep
from datetime import datetime


async def main():

    # chroma_function.delete_collection("news")
    # print(chroma_function.peek_collection("news"))

    # 读取文本
    file_name = "data/documents_dup_part_1_part_1_short"
    news_list = document_parser.file_reader(file_name)

    collection_name = "news"
    collection_description = "This collection contains news from 2023."

    user_command = input("Add or Query? ")
    if user_command.casefold() == "add":
        # 创建collection
        # embedding_function = llm_embedding.langchain_embed_model
        chroma_function.create_collection(collection_name, collection_description)

        # llm解析，提取，存入chroma数据库
        for news in news_list:
            ids = text_prep.generate_rand_id()

            embeddings = llm_embedding.langchain_embed_model.embed_documents(news)

            filled_title_prompt = llm_provider.fill_prompt(prompt.title_prompt, news)
            title = str(await llm_provider.call_llama(filled_title_prompt))

            filled_keywords_prompt = llm_provider.fill_prompt(prompt.keywords_prompt, news)
            keywords = str(await llm_provider.call_llama(filled_keywords_prompt))

            created_by = text_prep.generate_rand_name()
            created_at = text_prep.generate_rand_time(datetime(2024, 1, 1), datetime(2025, 1, 1))

            metadatas = text_prep.generate_metadata(title, keywords, created_by, created_at)

            chroma_function.add_data(collection_name, ids, embeddings, news, metadatas)

        # print(chroma_function.peek_collection("news"))
    else:
        # result = chroma_function.query_collection(collection_name, query, query_text, query_include,result_number)
        # print(result['metadatas']['title'])
        # print(result['metadatas']['keywords'][0])
        # print(result['documents'][0])

        query = "有没有名人相关的新闻？"
        query_text = "Query 1"
        result_include = ["documents", "metadatas"]
        result_number = 1
        collection = chroma_function.get_collection(collection_name)
        result = collection.query(
            query_embeddings=llm_embedding.langchain_embed_model.embed_query(query),
            query_texts=[query_text],
            # include=result_include,
            n_results=result_number
        )
        # print(result)
        print(result['metadatas'][0][0]['title'])
        print(result['metadatas'][0][0]['keywords'])
        print(result['documents'][0])


if __name__ == '__main__':
    asyncio.run(main())