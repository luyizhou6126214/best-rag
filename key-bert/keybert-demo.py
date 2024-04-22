#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/22 08:57
@Author  :   luyizhou
@Desc    :   
"""
from sklearn.feature_extraction.text import CountVectorizer
import jieba
from keybert import KeyBERT

def tokenize_zh(text):
    words = jieba.lcut(text)
    return words

vectorizer = CountVectorizer(tokenizer=tokenize_zh)



kw_model = KeyBERT()
doc = '请问最近的大盘趋势'

keywords = kw_model.extract_keywords(doc, vectorizer=vectorizer)
print(keywords)
