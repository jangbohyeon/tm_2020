import re
import csv

print(len(word_result_20200801))
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

