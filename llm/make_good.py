#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/16 10:09
@Author  :   luyizhou
@Desc    :   
"""
import json
import requests
from pprint import pprint


def chat(input):
    payload = json.dumps({
        "model": "showcai-13b",
        # "model": "deepseek",
        # "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "user",
                "content": input
            }
        ],
        "stream": False
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer sk-yqyDwbVVMgQJKlFU133d3c25E3A745E5Aa6a4b9b2dB6Ec0c',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    url = 'https://sg.hirenyi.com/v1/chat/completions'
    response = requests.post(url, data=payload, headers=headers)
    response.encoding = response.apparent_encoding
    result = response.json()
    answer = result.get('choices')[0].get('message').get('content')
    return answer


if __name__ == '__main__':

    question = """你是一位专业的证券行业投资顾问，现在需要你判断投顾人员的问题所表达的意图与以下意图选项中的哪个最匹配，并按照要求输出。
    
意图选项（格式说明：id-意图内容【意图解释】）：
1-持仓查询【包括明确提到查询客户持仓、客户抱怨持仓亏损】；
2-其他未知意图【包括闲聊、寒暄、礼貌用语、总结信息等】；
3-业务咨询【包括咨询投资建议、推荐产品、持仓分析、行情咨询、金融知识咨询、金融业务办理流程咨询（怎么开户、怎么购买、怎么定投、风险测评等）】；

【要求】
1.请根据意图解释的内容，优先与1和3意图进行比对和匹配。
2.当投顾问题中明确提到查询客户持仓时，才选择意图3；
3.如果1和3意图都不匹配，再匹配意图2；
4.必须且仅匹配一个意图；
5.必须按照下方输出格式要求进行输出，不要输出多余内容。

【输出格式要求】
如果是意图1，则输出：{"intentions":[{"intentionType":"1"}]}
如果是意图2，则输出：{"intentions":[{"intentionType":"2"}]}
如果是意图3，则输出：{"intentions":[{"intentionType":"3"}]}


【投顾问题】：
我想知道茅台的股票有投资价值么"""




    answer = chat(question)
    print(answer)
