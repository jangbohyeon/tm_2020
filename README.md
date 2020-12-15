# Textmining Project(Team Project)
>SoonChunHyang University, Department of BigData Engineering
>member : Jang Bo Hyeon, Lee Ga Hyun

--------------------
## Project explanation
>요즘은 하루에 1,000~10,000건의 기사가 쏟아져나오는데 우리는 모든 기사를 다 읽어볼 수 없다. 너무 많은 하루의 기사들을 한눈에 볼 수 있다면 얼마나 좋을까라고 생각되어 이 프로젝트를 시작하게 되었다.


### 분석
##### 데이터
- 빅카인즈(https://www.bigkinds.or.kr/) 사이트에서 데이터를 csv파일로 가져왔다.
- 기사의 본문(내용)은 크롤링 진행했다.
    - csv 파일의 기사를 확인한 결과, 기사의 본문(내용)이 일부만 나타남. 

#####  데이터 전처리
1. vocabulary
- 기사의 제목 데이터로 진행했다.
- nltk의 태그들 중 okt 태거를 사용했다,
- 단어 전처리 : 불용어 제거, 중복된 단어 제거, 한글자 제거, 의미없는 숫자만 존재하는 단어 제거
   
#####  데이터 분석
1. Document-Term matrix(DTM) : (행-기사, 열-vocabulary)
- DTM을 사용하여 등장 빈도 수가 높은 vocabulary 단어를 구했다.
2. TF-IDF 만들기

#####  요약
- 뉴스기사들을 수집하여 코사인 유사도를 사용하여 기사들의 유사도를 측정한다.
- 유사도가 0.7이상인 기사들을 모아 요약한다.  

#####   시각화
1. wordcloud
- DTM을 사용하여 만들었다.
- 'NanumBarunGothic.ttf' : 한글 인식 폰트 
2. HTML
- 한 페이지로 뉴스 기사의 keyword를 입력하여 요약된 기사내용을 읽을 수 있다.

#####  참고자료
> 불용어
>    - https://bab2min.tistory.com/544
>    - https://www.ranks.nl/stopwords/korean