# This file opens and reads a file
# 此文件用于文件的基础读取

def file_reader() -> list:
    with open("documents_dup_part_1_part_1") as f:
        news:list[str] = f.read().splitlines()
        return news
        # print(type(f.read()))