#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/17 09:35
@Author  :   luyizhou
@Desc    :   
"""
from textrank4zh import TextRank4Keyword

text = "被评过3次以上金牛奖的基金？"
tr4w = TextRank4Keyword()

tr4w.analyze(text=text, lower=True, window=2)

print( '关键词：' )
for item in tr4w.get_keywords(20, word_min_len=1):
    print(item.word, item.weight)