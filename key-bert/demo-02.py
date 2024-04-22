#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/16 15:55
@Author  :   luyizhou
@Desc    :   
"""
from keybert import KeyBERT

doc = "请问最近的融资融券情况？"
doc = "这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。答谢宴于晚上8点开始。"
kw_model = KeyBERT()
keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 1), highlight=True)
print(keywords)