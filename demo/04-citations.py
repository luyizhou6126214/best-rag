#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/12 15:09
@Author  :   luyizhou
@Desc    :
"""
import os
from operator import itemgetter
from typing import List

import bs4
from langchain_community.retrievers.wikipedia import WikipediaRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_core.documents import Document


os.environ['OPENAI_API_KEY'] = 'sk-yqyDwbVVMgQJKlFU133d3c25E3A745E5Aa6a4b9b2dB6Ec0c'
os.environ['OPENAI_BASE_URL'] = 'https://sg.hirenyi.com/v1'

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__64d99d8853044816a31a8eb9cab98c15"


llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)

wiki = WikipediaRetriever(top_k_results=6, doc_content_chars_max=2000)

qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        ("human", "{question}")
    ]
)

prompt.pretty_print()


def format_docs(docs: List[Document]) -> str:
    """
    转换document文档为字符串
    :param docs:
    :return:
    """
    formatted = [
        f"Article Title: {doc.metadata['title']}\nArticle Snippet: {doc.page_content}"
        for doc in docs
    ]
    return "\n\n" + "\n\n".join(formatted)

format = itemgetter("docs") | RunnableLambda(format_docs)

answer = prompt | llm | StrOutputParser()

chain = (
    RunnableParallel(question=RunnablePassthrough(), docs=wiki)
    .assign(context=format)
    .assign(answer=answer)
    .pick(["answer", "docs"])
)

res = chain.invoke("how fast are cheetahs")

from pprint import pprint
pprint(res)

