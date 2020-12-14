from math import log 

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
        tf_result[-1].append(tf(token,doc))

    
dtm_20200801 = pd.DataFrame(tf_result,columns = VOCA_20200801)

idf_result = []
for j in range(len(VOCA_20200801)):
    token = VOCA_20200801[j]
    idf_result.append(idf(token))
    
idf_ = pd.DataFrame(idf_result,index = VOCA_20200801, columns = ['IDF'])


from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_20200801 = TfidfVectorizer(min_df=2,sublinear_tf=True).fit(cnews_20200801['내용'])
print(tfidf_20200801.transform(cnews_20200801['내용']).toarray())
print(tfidf_20200801.vocabulary_)

