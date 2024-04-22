#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/2/29 14:09
@Author  :   luyizhou
@Desc    :   openai标准接口会话
"""
import time
from openai import OpenAI


api_key = 'sk-yqyDwbVVMgQJKlFU133d3c25E3A745E5Aa6a4b9b2dB6Ec0c'
base_url = 'https://sg.hirenyi.com/v1'
client = OpenAI(api_key=api_key, base_url=base_url)


def get_related_question_call(query, model, max_tokens=1024, temperature=0.9):
    """
    获取指定问题的关联问题
    Args:
        query:
        model:
        max_tokens:
        temperature:

    Returns:

    """
    _more_questions_prompt_v2 = """
你是一位资深的语言专家。擅长从一段文本中提取关键字。

下面给定一段文本，请帮我提取出最核心的关键字。
关键字必须是原始文本中的字或词，不允许添加不存在的字。
单个关键字不要超过4个字。需要返回最多3个关键字，并以列表[]格式返回，不要有多余的文字，格式参照下方的示例。

【示例问题】：请问最近的融资融券情况？
【示例答案】：["融资融券", "融资", "融券"]

以下是原始问题：
"""
    messages = []
    messages.append({"role": "system", "content": _more_questions_prompt_v2})
    messages.append({"role": "user", "content": query})
    function_descriptions = [
        {
            "name": "get_keyword",
            "description": "Extract keywords from the original document",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword-1": {
                        "type": "string",
                        "description": "the most core keywords in the text,No more than 4 words",
                    },
                    "keyword-2": {
                        "type": "string",
                        "description": "the most core keywords in the text,No more than 4 words",
                    },
                    "keyword-3": {
                        "type": "string",
                        "description": "the most core keywords in the text,No more than 4 words",
                    }
                },
                "required": ["keyword-1", "keyword-2", "keyword-3"],
            }
        }
    ]
    llm_response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        stream=False,
        temperature=temperature,
        function_call="auto",
        functions=function_descriptions
    )
    return llm_response.choices[0].message.function_call.arguments


if __name__ == '__main__':
    query = '被评过3次以上金牛奖的基金'
    query = '我想吃饭'
    data = get_related_question_call(query, "gpt-3.5-turbo-16k")
    print(data)
    # import json
    # data = json.loads(data.strip())
    # related_question_list = [{"question": value} for value in data.values()]
    # print(related_question_list)
