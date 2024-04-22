import requests


url = 'https://aitest.showcai.com.cn:27443/dwgpt/riskSearch/chat'

payload = {
    "query": "请问最近的融资融券情况",
    "appKey": "a9b3c2e4f1g5h7j",
    "md5Info": "7d2a8190e9afb4e398b87b5b71fa6c9e",
    "timestamp": 1713417261,
    "signFields": [
        "query",
        "appKey",
        "timestamp"
    ]
}
response = requests.post(url, json=payload, stream=True)

if response.status_code == 200:
    for chunk in response.iter_lines():
        print(chunk.decode('utf-8'))
else:
    print("Error:", response.status_code)



