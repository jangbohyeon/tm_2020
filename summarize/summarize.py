import pandas as pd
import os
import sys
import re

cfile_20200801 = pd.read_excel('../data_files/Crawling_20200801-20200801.xlsx')
cfile_20200801 = pd.DataFrame(cfile_20200801)

cnews_20200801 = cfile_20200801
cnews_20200801.columns = ['num', '내용']
# '제목'열에서 na가 있으면 해당 행 삭제
cnews_20200801 = cnews_20200801.dropna(subset=['내용'])
# row번호 리셋하기
cnews_20200801 = cnews_20200801.reset_index()

def cleaning_tx(m_news):
    #이메일 지우기
    m_news = re.sub('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', '', m_news)
    #.replace(',','').replace('.','').replace('"','').replace('!','').replace('?','')
    m_news = m_news.replace('\n',' ').replace('\t',' ').replace('(','').replace(')','').replace('[','').replace(']','').replace('.','. ').casefold()
    #\xa0는 줄바꿈을 의미
    m_news = re.sub('[-=+#/\:^$@*\"※~&ㆍ』\\‘|\(\)\[\]\<\>`\'…》]', '', m_news)
    complete_cleaning = re.sub('[▷▶◀◁◆■□▲◆●◎○△◇]', '', m_news)
    
    return complete_cleaning


from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_cosine_sim(str): 
    vectors = [t for t in get_vectors(str)]
    return cosine_similarity(vectors)
    
def get_vectors(str):
    text = [t for t in str]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


# In[ ]:


cos_sim = get_cosine_sim(cnews_20200801['내용'])

clean_news = cnews_20200801['내용']

news_cos_sim = []
for num in range(0, len(cos_sim)):
    for comp in range(0, num+1):
        if num != comp and cos_sim[num][comp] > 0.7:
            #num 행, comp 열
            news_cos_sim += [comp]

from gensim.summarization.summarizer import summarize

def news_summary(sent_num=0.5):
    voca_word = []
    origin_news_num = []
    summary = []
    for list_idx, n_news in enumerate(tfidf_news):
        #wd는 vocabulary 단어, tfidf는 tfidf계산된 값
        for wd, tfidf in n_news:
            if tfidf > sent_num:
                voca_word += [(wd, list_idx)]
                origin_news_num += [list_idx]
    
    origin_news_num.sort()
    origin_news_num = set(origin_news_num)

    # 위 for문에서 기사를 통으로 가져왔으므로 summarize
    for news in cnews_20200801['내용'][origin_news_num]:
        news_c = cleaning_tx(news)
        summary += [summarize(news_c, ratio=0.1)]

    return summary

"""
#요약을 두번하는 버전
def news_summary(sent_num=0.5):
    voca_word = []
    origin_news_num = []
    for list_idx, n_news in enumerate(tfidf_news):
        #wd는 vocabulary 단어, tfidf는 tfidf계산된 값
        for wd, tfidf in n_news:
            if tfidf > sent_num:
                voca_word += [(wd, list_idx)]
                origin_news_num += [list_idx]
    
    origin_news_num.sort()
    origin_news_num = set(origin_news_num)
    
    summary = ''
    for news in cnews_20200801['내용'][origin_news_num]:
        news_c = cleaning_tx(news)
        summary += summarize(news_c, ratio=0.1) + ' '
    
    summary_news = summarize(summary, ratio=0.1)

    return summary_news
"""

summarize_20200801 = news_summary()
summarize_20200801


def choose_word(word, freq=3):
    word_idx = VOCA_20200801.index(word)
    
    news_idx = []
    #tf_result : 기사별로 vocabulary의 등장빈도수를 계산한 리스트(리스트 in 리스트 형태)
    for num in range(0, len(tf_result)):
        if tf_result[num][word_idx] > freq and num not in news_cos_sim:
            news_idx.append(num)
    
    summary = ''
    for news in clean_news[news_idx]:
        news_c = cleaning_tx(news)
        summary += summarize(news_c, ratio=0.1) + ' '
    
    
    summary_news = summarize(summary, ratio=0.1)
    
    return summary_news

#after_sum = choose_word('코로나', 5)