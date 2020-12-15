import pandas as pd
import os
import sys
from konlpy.tag import Okt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import csv
from math import log
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.summarization.summarizer import summarize
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import stylecloud
import numpy as np
from PIL import Image


cfile_20200801 = pd.read_excel('./data_files/Crawling_20200801-20200801.xlsx')
cfile_20200801 = pd.DataFrame(cfile_20200801)
cnews_20200801 = cfile_20200801
cnews_20200801.columns = ['num', '내용']
cnews_20200801 = cnews_20200801.dropna(subset=['내용'])
cnews_20200801 = cnews_20200801.reset_index()

file_20200801 = pd.read_excel('./data_files/NewsResult_20200801-20200801.xlsx')
file_20200801 = pd.DataFrame(file_20200801)
columns_name = ['일자', '제목', '본문', '인물', '기관', '키워드', '특성추출(가중치순 상위 50개)', 'URL']

file_20200801 = file_20200801[columns_name]
news_20200801 = file_20200801

news_20200801 = news_20200801.dropna(subset=['제목'])
news_20200801 = news_20200801.reset_index()

for i in range(0,len(news_20200801)):
    news_20200801['제목'][i] = news_20200801['제목'][i].replace(',','').replace('\n','').replace('.','').\
    replace('"','').replace('!','').replace('(',' ').replace(')','').replace('?','').casefold()

word_20200801 = []
for i in range(len(news_20200801)):
    word_20200801 += (word_20200801, word_tokenize(news_20200801['제목'][i]))


okt = Okt()
okt_word_20200801 = []
for i in range(len(news_20200801)):
    okt_word_20200801 +=  okt.pos(news_20200801['제목'][i])

for i, k in enumerate(okt_word_20200801):
    if k[1].find('J') == 0 or k[1].find('P') or k[1].find('F') == 0:
        okt_word_20200801.pop(i)

stop_words = []
with open('./stopwordlist/stopwords_list1.txt', 'r') as file1,\
        open('./stopwordlist/stopwords_list2.txt', 'r') as file2:
    for text1 in file1:
        stop_words.append(text1.strip('\n'))
    print(len(stop_words))
    for text2_1 in file2:
        text2 = text2_1.split('\t')
        stop_words.append(text2[0].strip('\n'))
    print(len(stop_words))

stopwords_set = set(stop_words)
stop_words = list(stopwords_set)


word_result_20200801 = []
for w, pos in okt_word_20200801:
    if w not in stop_words:
        word_result_20200801.append(w)

for i in word_result_20200801:
    if len(i) == 1:
        word_result_20200801.remove(i)


set_20200801 = set(word_result_20200801)
VOCA_20200801 = list(set_20200801)

for i in voca_20200801:
    if len(i) == 1:
        VOCA_20200801.remove(i)

for i in voca_20200801:
    if len(i) == 1:
        voca_20200801.remove(i)

imsi = []
for tx in voca_20200801:
    hangul = re.compile('[ㄱ-ㅣ가-힣a-zA-Z]+')
    imsi.append(hangul.findall(tx))

VOCA_20200801 = []
for k in range(0, len(voca_20200801)):
    if imsi[k] != []:
        VOCA_20200801.append(voca_20200801[k])

with open('./data_files/title_voca_okt.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(VOCA_20200801)


N = len(cnews_20200801)
def tf(token, doc):
    return doc.count(token)
def idf(token):
    df = 0
    for doc in list(cnews_20200801['내용']):
        df += token in doc
    return log(N / (df + 1))
def tf_idf(token, doc):
    return tf(token, doc) * idf(token)

tf_result = []
for i in range(N):
    tf_result.append([])
    doc = cnews_20200801['내용'][i]
    for j in range(len(VOCA_20200801)):
        token = VOCA_20200801[j]
        tf_result[-1].append(tf(token, doc))

dtm_20200801 = pd.DataFrame(tf_result, columns=VOCA_20200801)

idf_result = []
for j in range(len(VOCA_20200801)):
    token = VOCA_20200801[j]
    idf_result.append(idf(token))

idf_ = pd.DataFrame(idf_result, index=VOCA_20200801, columns=['IDF'])

tfidf_20200801 = TfidfVectorizer(min_df=2, sublinear_tf=True).fit(cnews_20200801['내용'])


tfidf_vec = TfidfVectorizer()
sp_matrix = tfidf_vec.fit_transform(cnews_20200801['내용'])

tfidf_dict = defaultdict(lambda: 0)
for idx, feature in enumerate(tfidf_vec.get_feature_names()):
    tfidf_dict[feature] = idx

def news_tfidf(cnews):
    news2tfidf = []
    for i, sent in enumerate(cnews):
        news2tfidf += [[(token, sp_matrix[i, tfidf_dict[token]]) for token in VOCA_20200801 if
                        sp_matrix[i, tfidf_dict[token]] > 0]]
    return news2tfidf

tfidf_news = news_tfidf(cnews_20200801['내용'])

def cleaning_tx(m_news):
    m_news = re.sub('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', '', m_news)
    m_news = m_news.replace('\n', ' ').replace('\t', ' ').replace('(', '').replace(')', '').\
        replace('[', '').replace(']', '').replace('.', '. ').casefold()
    m_news = re.sub('[-=+#/\:^$@*\"※~&ㆍ』\\‘|\(\)\[\]\<\>`\'…》]', '', m_news)
    complete_cleaning = re.sub('[▷▶◀◁◆■□▲◆●◎○△◇]', '', m_news)
    return complete_cleaning

def get_cosine_sim(str):
    vectors = [t for t in get_vectors(str)]
    return cosine_similarity(vectors)

def get_vectors(str):
    text = [t for t in str]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()

cos_sim = get_cosine_sim(cnews_20200801['내용'])
clean_news = cnews_20200801['내용']
news_cos_sim = []
for num in range(0, len(cos_sim)):
    for comp in range(0, num+1):
        if num != comp and cos_sim[num][comp] > 0.7:
            news_cos_sim += [comp]

def news_summary(sent_num=0.5):
    voca_word = []
    origin_news_num = []
    summary = []
    for list_idx, n_news in enumerate(tfidf_news):
        for wd, tfidf in n_news:
            if tfidf > sent_num:
                voca_word += [(wd, list_idx)]
                origin_news_num += [list_idx]

    origin_news_num.sort()
    origin_news_num = set(origin_news_num)

    for news in cnews_20200801['내용'][origin_news_num]:
        news_c = cleaning_tx(news)
        summary += [summarize(news_c, ratio=0.1)]
    return summary

summarize_20200801 = news_summary()

def choose_word(word, freq=3):
    word_idx = VOCA_20200801.index(word)

    news_idx = []
    for num in range(0, len(tf_result)):
        if tf_result[num][word_idx] > freq and num not in news_cos_sim:
            news_idx.append(num)

    summary = ''
    for news in clean_news[news_idx]:
        news_c = cleaning_tx(news)
        summary += summarize(news_c, ratio=0.1) + ' '

    summary_news = summarize(summary, ratio=0.1)

    return summary_news


word_count = dtm_20200801.sum()
word_dict = dict(word_count)

mask = np.array(Image.open('image.jpg'))
wc = WordCloud(mask=mask, max_font_size=100,
               max_words=40, background_color="white",
               font_path='./visualization/NanumBarunGothic.ttf')
plt.imshow(wc.generate_from_frequencies(word_dict), interpolation="bilinear")
plt.axis("off")
