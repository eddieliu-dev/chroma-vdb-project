# This file opens and reads a file
# 此文件用于文件的基础读取

def file_reader(file_name) -> list:
    with open(file_name) as f:
        news:list[str] = f.read().splitlines()
        return news
        # print(type(f.read()))