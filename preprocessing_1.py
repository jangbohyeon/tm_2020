import pandas as pd
import os
import sys

mod = sys.modules[__name__]
def excel_reader():
    # 해당 경로에 있는 .xlsx 포맷의 파일이름을 리스트로 가져오기
    path = "/home/u1026/tm_2020/"
    file_list = os.listdir(path)
    exfile_list = [i for i in file_list if os.path.splitext(i)[-1] == ".xlsx"]

    # 파일이름을 split 해 해당 파일의 날짜 리스트로 가져오기
    fname_list = []
    for i in range(len(exfile_list)):
        fname_list += [exfile_list[i].split("-")[0].split("_")[1]]

    # exfile_list에 있는 엑셀파일 모두 읽어오기
    for k in range(len(exfile_list)):
        file_locate = path + exfile_list[k]
        setattr(mod, 'file_{}'.format(fname_list[k]), pd.read_excel(file_locate))

excel_reader()


#190801 뉴스 데이터 불러오기
file_0801 = pd.read_csv('./NewsResult_20190801-20190801.csv')

#필요한 column들만 추출
columns_name = ['일자', '제목', '인물', '기관', '키워드', '특성추출(가중치순 상위 50개)', '본문', 'URL']
file_190801 = file_190801[columns_name]

news_190801 = file_190801
#내용 : 본문과 제목을 합친 텍스트 column
news_190801['내용'] = file_190801.iloc[:, 1:3].sum(1)


#word_tokenize : space 단위와 구두점(punctuation)을 기준으로 토큰화(Tokenize)
from nltk.tokenize import word_tokenize

word_190801 =[]
for i in range(len(news_190801)):
    word_190801 += (word_190801, word_tokenize(news_190801['내용'][i]))

len(word)

