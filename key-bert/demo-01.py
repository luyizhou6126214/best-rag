#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/16 15:26
@Author  :   luyizhou
@Desc    :   
"""
import openai
from keybert.llm import OpenAI
from keybert import KeyLLM


api_key = 'sk-yqyDwbVVMgQJKlFU133d3c25E3A745E5Aa6a4b9b2dB6Ec0c'
base_url = 'https://sg.hirenyi.com/v1'


client = openai.OpenAI(api_key=api_key, base_url=base_url)
llm = OpenAI(client, model='gpt-3.5-turbo-16k', chat=True)
kw_model = KeyLLM(llm)

documents = "被评过3次以上金牛奖的基金？"
    # "请问最近的融资融券情况？"
    # "请问最近的大盘趋势"
    # "这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。答谢宴于晚上8点开始。"


keywords = kw_model.extract_keywords(documents, check_vocab=True, threshold=.75)

print(keywords)