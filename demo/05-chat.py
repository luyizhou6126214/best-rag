#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/23 15:48
@Author  :   luyizhou
@Desc    :   
"""
import os
from pprint import pprint

from typing import Dict
from langchain_core.runnables import RunnablePassthrough

from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.web_base import WebBaseLoader

from langchain_community.vectorstores.chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain


os.environ['OPENAI_API_KEY'] = 'sk-yqyDwbVVMgQJKlFU133d3c25E3A745E5Aa6a4b9b2dB6Ec0c'
os.environ['OPENAI_BASE_URL'] = 'https://sg.hirenyi.com/v1'

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__64d99d8853044816a31a8eb9cab98c15"


llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)


# 抽取网页数据
loader = WebBaseLoader("http://theory.people.com.cn/BIG5/n1/2019/0428/c40531-31054034.html")
data = loader.load()

# 文本分割器
text_spilitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_spilitter.split_documents(data)

# embedding
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# retriever
retriever = vectorstore.as_retriever(k=4)

# docs = retriever.invoke("五四运动")
#
# pprint(docs)

question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user's questions based on the below context:\n\n{context}"
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

document_chain = create_stuff_documents_chain(llm, question_answering_prompt)

chat_history = ChatMessageHistory()
chat_history.add_user_message("五四运动")

# res = document_chain.invoke({
#     "messages": chat_history.messages,
#     "context": docs
# })
#
# pprint(res)


def parse_retriever_input(params: Dict):
    print('*' * 50)
    print(params)
    print('*' * 50)
    return params["messages"][-1].content


# 包含中间步骤
# retriever_chain = RunnablePassthrough.assign(
#     context=parse_retriever_input | retriever
# ).assign(
#     answer=document_chain
# )


# 不包含中间不住，只输出答案
retriever_chain = RunnablePassthrough.assign(
    context=parse_retriever_input | retriever
) | document_chain


res = retriever_chain.invoke(
    {
        "messages": chat_history.messages,
    }
)

pprint(res)
