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
from langchain_core.runnables import RunnablePassthrough
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


contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is.
"""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ]
)
history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)


qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# chat_history = []
# question_1 = "苏州的产业发展"
# ai_answer_1 = rag_chain.invoke({"input": question_1, "chat_history": chat_history})
# print(ai_answer_1)
#
# chat_history.extend([HumanMessage(content=question_1), ai_answer_1["answer"]])
#
# question_2 = "苏州有哪些举措"
# ai_answer_2 = rag_chain.invoke({"input": question_2, "chat_history": chat_history})
# print(ai_answer_2)

question_1 = "苏州的产业发展"
question_2 = "有哪些举措"
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer"
)


res1 = conversational_rag_chain.invoke(
    {"input": question_1},
    config={
        "configurable": {"session_id": "abc123"}
    }
)

print(res1['answer'])


res2 = conversational_rag_chain.invoke(
    {"input": question_2},
    config={
        "configurable": {"session_id": "abc123"}
    }
)

print(res2['answer'])












# prompt = hub.pull("rlm/rag-prompt")

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)
#
# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )
#
# res = rag_chain.invoke("苏州的产业发展")
#
# print(res)

