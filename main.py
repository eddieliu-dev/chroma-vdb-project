# This is the main file of the project. 此文件是项目的主文件
# All the operations will eventually run here

from chroma import chroma_client, chroma_function
from llm import llm_embedding, llm_provider
import document_parser, prompt, text_prep
from datetime import datetime


def main():

    # chroma_function.delete_collection("news")
    # print(chroma_function.peek_collection("news"))

    # 读取文本
    news_list = document_parser.file_reader()

    # 创建collection
    collection_name = "news"
    collection_description = "This collection contains news from 2023."
    # embedding_function = llm_embedding.langchain_embed_model
    chroma_function.create_collection(collection_name, collection_description)

    # llm解析，提取，存入chroma数据库
    for news in news_list:
        ids = text_prep.generate_rand_id()

        embeddings = llm_embedding.langchain_embed_model.embed_documents(news)

        filled_title_prompt = llm_provider.fill_prompt(prompt.title_prompt, news)
        title = llm_provider.call_llama(filled_title_prompt)

        filled_keywords_prompt = llm_provider.fill_prompt(prompt.keywords_prompt, news)
        keywords = llm_provider.call_llama(filled_keywords_prompt)

        created_by = text_prep.generate_rand_name()
        created_at = text_prep.generate_rand_time(datetime(2024, 1, 1), datetime(2025, 1, 1))

        metadatas = text_prep.generate_metadata(title, keywords, created_by, created_at)

        chroma_function.add_data(collection_name, ids, embeddings, news, metadatas)

    print(chroma_function.peek_collection("news"))


if __name__ == '__main__':
    main()
