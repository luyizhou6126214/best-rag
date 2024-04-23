#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/16 10:09
@Author  :   luyizhou
@Desc    :   
"""
import json
import requests


def chat(input):
    payload = json.dumps({
        "model": "showcai-13b",
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
    query = "你是哪家公司研发的"
    print(chat(query))

    # import pandas as pd
    # df = pd.read_excel(r"/Users/luyizhou/Desktop/模型命中效果对比_光子_昆仑_幻方_秀财.xlsx")
    #
    # # df = df.head(1)
    # temp_result = []
    # try:
    #     for index,row in df.iterrows():
    #         question = row['问题']
    #         print('=' * 50)
    #         print(f'==> index: {index}')
    #         print(f'==> Q: {question}')
    #         answer = chat(question)
    #         print(f'==> A: {answer}')
    #         print('\n\n')
    #         df.at[index, 'showcai-13b'] = answer
    #         temp_result.append({'quesion': question, 'answer': answer})
    #     df.to_excel('output.xlsx', index=False)
    # except Exception as e:
    #     print(str(e))
    # finally:
    #     with open('temp.json', 'w') as f:
    #         f.write(json.dumps(temp_result, ensure_ascii=False))
