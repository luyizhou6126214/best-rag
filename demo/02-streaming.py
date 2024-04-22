#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/12 15:09
@Author  :   luyizhou
@Desc    :
"""
import os
from typing import TypedDict, List, Optional, Dict, Any

import bs4
from langchain import hub
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tracers.log_stream import LogEntry
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.web_base import WebBaseLoader

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage



os.environ['OPENAI_API_KEY'] = 'sk-yqyDwbVVMgQJKlFU133d3c25E3A745E5Aa6a4b9b2dB6Ec0c'
os.environ['OPENAI_BASE_URL'] = 'https://sg.hirenyi.com/v1'

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__64d99d8853044816a31a8eb9cab98c15"


llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)


loader = WebBaseLoader(
    web_path=("http://www.subaonet.com/2024/xwzt/xsdxzwxpz/xsdxzwxpz_xzw/0412/873184.shtml"),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("list_neiA fontSizeSmall BSHARE_POP article-content", )
        )
    ),
)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()


contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

# 设置prompt模版
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ]
)

# 组装chain
contextualize_q_chain = (contextualize_q_prompt | llm | StrOutputParser()).with_config(
    tags=["contextualize_q_chain"]
)

# 根据问题问答、检索文本回答的【提示词】
qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ]
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def contextualized_question(input: dict):
    if input.get("chat_history"):
        return contextualize_q_chain
    else:
        return input["question"]

rag_chain = (
    RunnablePassthrough.assign(context=contextualize_q_chain | retriever | format_docs)
    | qa_prompt
    | llm
)

class RunState(TypedDict):
    id: str
    """ID of the run."""
    streamed_output: List[Any]
    """List of output chunks streamed by Runnable.stream()"""
    final_output: Optional[Any]
    """Final output of the run, usually the result of aggregating (`+`) streamed_output.
    Only available after the run has finished successfully."""

    logs: Dict[str, LogEntry]
    """Map of run names to sub-runs. If filters were supplied, this list will
    contain only the runs that matched the filters."""


import nest_asyncio

nest_asyncio.apply()

from langchain_core.messages import HumanMessage

chat_history = []

question = "苏州的产业发展?"
ai_msg = rag_chain.invoke({"question": question, "chat_history": chat_history})
chat_history.extend([HumanMessage(content=question), ai_msg])

second_question = "有哪些举措?"
ct = 0
async for jsonpatch_op in rag_chain.astream_log(
    {"question": second_question, "chat_history": chat_history},
    include_tags=["contextualize_q_chain"],
):
    print(jsonpatch_op)
    print("\n" + "-" * 30 + "\n")
    ct += 1
    # if ct > 20:
    #     break










# qa_system_prompt = """You are an assistant for question-answering tasks. \
# Use the following pieces of retrieved context to answer the question. \
# If you don't know the answer, just say that you don't know. \
# Use three sentences maximum and keep the answer concise.\
#
# {context}"""
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", qa_system_prompt),
#         ("human", "{input}")
#     ]
# )
#
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)
#
# rag_chain = (
#     RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
#     | prompt
#     | llm
#     | StrOutputParser()
# )
#
# rag_chain_with_source = RunnableParallel(
#     {"context": retriever, "input": RunnablePassthrough()}
# ).assign(answer=rag_chain)
#
#
# query = "苏州的产业发展"
#
# for chunk in rag_chain_with_source.stream(query):
#     print(chunk)

