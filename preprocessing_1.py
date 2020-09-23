import pandas as pd
file_0801 = pd.read_csv('~/tm_2020/NewsResult_20190801-20190801.csv')

print(file_190801.shape)

columns_name = ['일자', '제목', '인물', '기관', '키워드', '특성추출(가중치순 상위 50개)', '본문', 'URL']
file_190801 = file_190801[columns_name]
file_190801.head()

#본문과 제목 칼럼의 내용을 리스트로
title = file_190801.제목.tolist()
main_text = file_190801.본문.tolist()

#본문과 제목의 내용을 합친다.
titleandtext = []
for i in range(len(file_190801)):
    titleandtext += [title[i] + main_text[i]]

#기존의 title과 main_text 불러오기
print(title[0])
print(main_text[0])
#title과 main_text를 합친 것을 불러오기
print(titleandtext[0])
