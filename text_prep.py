# This file is for preparing the text and its relevant information for storage.
# 此文件用于准备储存文本数据
import random
from datetime import timedelta, datetime

import document_parser
import uuid

def generate_rand_name() -> str:
    lastnames = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨"
    firstnames = "伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全"
    lastname = random.choice(lastnames)
    firstname = random.choice(firstnames)+random.choice(firstnames)
    return lastname+firstname

def generate_rand_time(start, end) -> str:
    delta = end - start
    rand_second = random.randint(0, int(delta.total_seconds()))
    return str(start + timedelta(seconds=rand_second))

# Prepare text for storage. 准备储存文本 封装成方法
def records_prep() -> list:
    records = document_parser.file_reader()
    return records

def generate_rand_id() -> uuid:
    return uuid.uuid4()

def generate_metadata() -> dict:
    metadata = {
        "title": "titles to be added with LLM later",
        "keywords": [],  # to be added with LLM later
        "created_by": generate_rand_name(),
        "created_at": generate_rand_time(datetime(2024, 1, 1), datetime(2025, 1, 1))
    }
    return metadata