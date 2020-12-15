import os
import sys
sys.path.append('../precleaning/')
import precleaning_ip

news_20200801 = precleaning_ip.news_20200801

from konlpy.tag import Okt
okt = Okt()

okt_word_20200801 = []
for i in range(len(news_20200801)):
    okt_word_20200801 +=  okt.pos(news_20200801['제목'][i])

for i, k in enumerate(okt_word_20200801):
    if k[1].find('J') == 0 or k[1].find('P') or k[1].find('F') == 0:
        okt_word_20200801.pop(i)

stop_words = []
with open('../stopwordlist/stopwords_list1.txt', 'r') as file1, \
open('../stopwordlist/stopwords_list2.txt', 'r') as file2:
    for text1 in file1:
        stop_words.append(text1.strip('\n'))
    print(len(stop_words))
    for text2_1 in file2:
        text2 = text2_1.split('\t')
        stop_words.append(text2[0].strip('\n'))
    print(len(stop_words))

stopwords_set = set(stop_words)
stop_words = list(stopwords_set)


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

word_result_20200801 = []
for w, pos in okt_word_20200801:
    if w not in stop_words:
        word_result_20200801.append(w)

for i in word_result_20200801:
    if len(i) == 1:
        word_result_20200801.remove(i)
