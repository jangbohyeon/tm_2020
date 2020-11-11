from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas as pd


driver = webdriver.Chrome('C:/Users/pc/PycharmProjects/2020_practice/chromedriver.exe/')
driver.implicitly_wait(3)
driver.get('https://www.bigkinds.or.kr/')
driver.implicitly_wait(1)

def searchDate(sdate, edate):
    #기간 창 클릭
    driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[1]/button').click()

    BACKSPACE = '/ue003'

    start_date = driver.find_element_by_xpath('//input[@id="search-begin-date"]')
    #start date 넣기
    for i in range(1, 11):
        start_date.send_keys(Keys.BACKSPACE)
    start_date.send_keys(sdate)

    driver.implicitly_wait(3)

    end_date = driver.find_element_by_xpath('//input[@id="search-end-date"]')
    #end date 넣기
    for i in range(1, 11):
        end_date.send_keys(Keys.BACKSPACE)
    end_date.send_keys(edate)

    driver.implicitly_wait(3)

    #적용버튼 클릭
    driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[1]/div/div[5]/button[2]').click()
    driver.implicitly_wait(3)

searchDate('2020-08-01', '2020-08-01')
#검색버튼 클릭
driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[1]/span/button').click()
driver.implicitly_wait(5)


#해당 날짜의 기사수가 몇개인지 확인. 기사갯수에 따라 달라지는 페이지수 확인. 페이지수에 따라 달라지는 반복횟수 확인
news_cnt = str(driver.find_element_by_xpath('//*[@id="total-news-cnt"]').text)
news_cnt = news_cnt.replace(',', '')
if int(news_cnt) % 10 == 0:
    pages = int(news_cnt) // 10
else:
    pages = int(news_cnt) // 10 + 1
ppages = math.ceil(pages / 7)

text = []
#ppages-1번 반복
for repeat in range(1, ppages):
    #page는 2부터 8까지 클릭(반복)
    for page in range(2, 9):
        if page != pages:
            #페이지마다 기사 10개씩 크롤링 -> text에 리스트로 저장
            for i in range(1, 11):
                #기사 클릭
                path = '//*[@id="news-results"]/div[' + str(i) + ']/div[2]/h4'
                driver.find_element_by_xpath(path).click()

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                #기사의 내용 크롤링
                tx = soup.select('#news-detail-modal > div > div > div.modal-body > div')
                for k in tx:
                    text.append(k.getText().strip())

                #X버튼 클릭 -> 다시 다른 기사들이 있는 페이지로 이동
                driver.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[1]/button/span').click()
            time.sleep(5)

        else:
            #해당 페이지에 기사가 10개 아닌 경우(news_cnt를 10으로 나눈 나머지)만큼만 크롤링 -> text에 리스트로 저장
            n = int(news_cnt) % 10
            for i in range(1, n + 1):
                WebDriverWait(driver, 10)
                path = '//*[@id="news-results"]/div[' + str(i) + ']/div[2]/h4'
                driver.find_element_by_xpath(path).click()

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                tx = soup.select('#news-detail-modal > div > div > div.modal-body > div')
                for k in tx:
                    text.append(k.getText().strip())

                driver.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[1]/button/span').click()
            time.sleep(5)

        #페이지 이동 클릭
        page_path = '//*[@id="news-results-pagination"]/ul/li[' + str(page + 2) + ']/a'
        driver.find_element_by_xpath(page_path).click()
        #페이지 이동 로딩이 걸릴 수 있으므로 sleep을 걸어준다.
        time.sleep(10)

    time.sleep(10)


"""
#크롤링 완료 후 text를 엑셀파일로 저장 -> 추후에 다시 사용할 수 있도록(?)
import pandas as pd
news_20200801 = pd.DataFrame(text)
news_20200801.to_excel('news_20200801.xlsx')
"""
