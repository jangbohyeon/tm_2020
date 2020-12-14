#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from math import log #idf 계산을 위한 패키지
#tf-idf 함수 구현하기
N = len(news_20200801)

def tf(token, doc):
    return doc.count(token)

def idf(token):
    df = 0
    for doc in list(news_20200801['내용']):
        df += token in doc
    return log(N / (df + 1))

def tf_idf(token, doc):
    return tf(token, doc) * idf(token)


# In[ ]:


#tf : DTM을 데이터 프레임으로 저장하여 출력된 값임. (행-문서, 열-단어)
tf_result = []
for i in range(N):
    tf_result.append([])
    doc = news_20200801['내용'][i]
    for j in range(len(VOCA_20200801)):
        token = VOCA_20200801[j]
        tf_result[-1].append(tf(token,doc))

    
dtm_20200801 = pd.DataFrame(tf_result,columns = VOCA_20200801)
dtm_20200801


# In[ ]:


#idf 를 구하겠음
idf_result = []
for j in range(len(VOCA_20200801)):
    token = VOCA_20200801[j]
    idf_result.append(idf(token))
    
idf_ = pd.DataFrame(idf_result,index = VOCA_20200801, columns = ['IDF'])
idf_


# In[ ]:


#패키지를 이용하여 만든 tf-idf
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_20200801 = TfidfVectorizer(min_df=2,sublinear_tf=True).fit(news_20200801['내용'])
print(tfidf_20200801.transform(news_20200801['내용']).toarray())
print(tfidf_20200801.vocabulary_)

