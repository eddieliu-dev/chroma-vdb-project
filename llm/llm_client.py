# llm_client.py
#
# This file defines two main functions:
# - fill_prompt: inserts input text into a predefined prompt template.
# - call_llama: sends the prompt to a local LLM API (Ollama) and returns the generated response.
# The model used is "llama3.1:latest", and the API runs on localhost at port 11434.
#
# 此文件定义了两个主要函数：
# - fill_prompt：将输入文本填入预设的prompt模板中。
# - call_llama：将填好的prompt发送给本地 LLM 接口（Ollama），并返回生成结果。
# 使用的模型是 "llama3.1:latest"，API 运行在本地 11434 端口。

import aiohttp

API_URL = "http://localhost:11434/api/generate"

headers = {
    "Content-Type": "application/json",
}

def fill_prompt(prompt, text) -> str:
    filled_prompt = (
        prompt.replace("{{NEWS}}", text)
    )
    return filled_prompt

async def call_llama(filled_prompt) -> str:
    payload = {
        "model": "llama3.1:latest",
        # "messages": [
        #     {"role": "user", "content": filled_prompt},
        # ],
        "prompt": filled_prompt,
        "stream": False
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            resp_json = await resp.json()
            content = str(resp_json["response"])
        # print(resp_json)

    # print(content)
    # print(type(content))
    return content

# Testing code 测试代码：
# async def main():
#     title_prompt = """
#     你是一个专业的文本阅读AI模型，专门从事文本提取与总结工作。
#     请阅读以下string类型的输入, 并将文本总结为一个标题：
#     <news>
#     {{NEWS}}
#     </news>
#     在完成任务时，请遵守以下要求：
#     1.除标题外不要输出其他任何内容。
#     2.标题不超过10个字。
#     请以纯文本输出标题（不包含任何标签、标点、前缀）。
#     """
#     keywords_prompt = """
#     你是一个专业的文本阅读AI模型，专门从事文本提取与摘要工作。
#     请阅读以下string类型的输入，并提取能够代表文本内容的关键词：
#     <news>
#     {{NEWS}}
#     </news>
#     在完成任务时，请遵守以下要求：
#     1.除关键词外不要输出其他任何内容。
#     3.提取的关键词数量应为3到5个。
#     请以string list类型输出关键词，格式如 ["关键词1", "关键词2", "关键词3"]。
#     """
#     text = "2023-08-11 15:10，正文：中新网约翰内斯堡8月10日电 (记者 王曦)“中国-南非企业贸易对接会暨签约仪式”10日在南非约翰内斯堡举行。中国商务部部长王文涛、南非贸工部部长易卜拉欣·帕特尔、中国驻南非大使陈晓东、南非驻华大使谢胜文、金砖国家工商理事会南非理事会理事斯塔夫罗斯·尼古拉，以及南非贸工部高级官员和来自中南两国企业家代表280多人参加活动。王文涛表示，近年来，两国元首保持战略沟通，引领推动双边经贸合作取得长足发展。中南双边贸易稳步提升，双向投资规模扩大。当前，中国正在以高质量发展推进中国式现代化，将为包括南非在内的世界各国带来重要机遇，中南、中非经贸合作前景光明、大有可为。今年是中南建交25周年，也是金砖“南非年”。中方组织贸易促进团来南非开展进口采购，是落实两国元首共识的实际行动。愿通过此次活动，进一步挖掘双方合作潜力，拓展合作空间。中方坚持对外开放基本国策，稳步扩大制度型开放，不断提升贸易投资自由化便利化水平，愿继续积极扩大自各方进口。诚挚欢迎南非企业来华参加第六届进博会等展会，加大对南非优势特色产品的推介力度，进一步开拓中国市场。易卜拉欣·帕特尔表示，南中两国建交以来，双边经贸合作取得诸多务实成果，为两国关系进一步发展打下良好基础。"
#     filled_prompt = fill_prompt(keywords_prompt, text)
#     await call_llama(filled_prompt)
#
# if __name__ == "__main__":
#     asyncio.run(main())
