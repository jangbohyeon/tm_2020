import pandas as pd
import os
import sys

cfile_20200801 = pd.read_excel('../data_files/Crawling_20200801-20200801.xlsx')
cfile_20200801 = pd.DataFrame(cfile_20200801)
cnews_20200801.columns = ['num', '내용']
cnews_20200801 = cnews_20200801.dropna(subset=['내용'])
cnews_20200801 = cnews_20200801.reset_index()


file_20200801 = pd.read_excel('../data_files/NewsResult_20200801-20200801.xlsx')
file_20200801 = pd.DataFrame(file_20200801)
columns_name = ['일자', '제목', '본문', '인물', '기관', '키워드', '특성추출(가중치순 상위 50개)', 'URL']

file_20200801 = file_20200801[columns_name]
news_20200801 = file_20200801

news_20200801 = news_20200801.dropna(subset=['제목'])
news_20200801 = news_20200801.reset_index()

for i in range(0,len(news_20200801)):
    news_20200801['제목'][i] = news_20200801['제목'][i].replace(',','').replace('\n','').replace('.','').\
    replace('"','').replace('!','').replace('(',' ').replace(')','').replace('?','').casefold()

from nltk.tokenize import word_tokenize
word_20200801 = []
for i in range(len(news_20200801)):
    word_20200801 += (word_20200801, word_tokenize(news_20200801['제목'][i]))
