# record_helper.py
#
# This file contains helper functions for preparing text and metadata for storage.
# It includes functions to read text, generate random names, timestamps, UUIDs, and metadata dictionaries.
#
# 此文件包含用于准备文本和元数据的辅助函数。
# 包括读取文本、生成随机姓名、时间戳、UUID 以及元数据字典等功能。

import random, uuid
from datetime import timedelta, datetime


# Generate random chinese names 随机生成中文名
def generate_rand_name() -> str:
    lastnames = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨"
    firstnames = "伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全"
    lastname = random.choice(lastnames)
    firstname = random.choice(firstnames) + random.choice(firstnames)
    return lastname + firstname


# Generate random timestamps 随机生成时间戳
def generate_rand_time(start, end) -> str:
    delta = end - start
    rand_second = random.randint(0, int(delta.total_seconds()))
    return str(start + timedelta(seconds=rand_second))


# Read text by line for storage 按行读取文本，方便后续储存
def file_reader(file_name) -> list:
    with open(file_name) as f:
        records:list[str] = f.read().splitlines()
        return records
        # print(type(f.read()))


# Generate random id 生成随机id
def generate_rand_id() -> str:
    return str(uuid.uuid4())


# Generate metadata for storage 生成元数据，方便后续储存
def generate_metadata(title, keywords, who, when) -> dict:
    metadata = {
        "title": title,
        "keywords": keywords,
        "created_by": who,
        "created_at": when
    }
    return metadata
