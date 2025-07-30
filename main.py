# This is the main file of the project. 此文件是项目的主文件
# All the operations will eventually run here

from chroma import chroma_client, chroma_function
import document_parser


def main():
    print(document_parser.file_reader())


if __name__ == '__main__':
    main()
