# This file extracts titles and keywords using LLM and the appropriate prompt.
# 此文件通过LLM和prompt提取标题和关键字 用doubao方式调用

import asyncio
import aiohttp
import json

# import sys, os
# root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, root_path)
# import document_parser

API_URL = "http://localhost:11434/api/generate"

headers = {
    "Content-Type": "application/json",
}

def fill_prompt(prompt, text) -> str:
    filled_prompt = (
        prompt.replace("{{NEWS}}", text)
    )
    return filled_prompt

async def call_llama(filled_prompt):
    payload = {
        "model": "llama3.1",
        "messages": [
            {"role": "user", "content": filled_prompt},
        ],
        "stream": False
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            resp_json = await resp.json()
            content = resp_json["choices"][0]["message"]["content"]

    return content

# async def main():
#     await call_llama()
#
# if __name__ == "__main__":
#     asyncio.run(main())
