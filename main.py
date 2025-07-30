# This is the main file of the project. 此文件是项目的主文件
# All the operations will eventually run here

import chroma_client, chroma_function, document_parser, llm_embedding, llm_utils


def main():
    print(document_parser.file_reader())


if __name__ == '__main__':
    main()
