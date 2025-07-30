# This file is configuration of the embedding model.
# 此文件是embedding模型的基础配置

from sentence_transformers import SentenceTransformer
import document_parser

model = SentenceTransformer("BAAI/bge-large-zh-v1.5")

# sentences = [
#     # "The weather is lovely today.",
#     # "It's so sunny outside!",
#     # "He drove to the stadium."
#
# ]
# embeddings = model.encode(sentences)

# similarities = model.similarity(embeddings, embeddings)
# print(similarities.shape)
# [3, 3]