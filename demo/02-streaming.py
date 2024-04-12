#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/12 15:09
@Author  :   luyizhou
@Desc    :
"""
import os
import bs4
from langchain import hub
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.runnables.history import RunnableWithMessageHistory
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

qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        ("human", "{input}")
    ]
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain_with_source = RunnableParallel(
    {"context": retriever, "input": RunnablePassthrough()}
).assign(answer=rag_chain)


query = "苏州的产业发展"

for chunk in rag_chain_with_source.stream(query):
    print(chunk)

