'''
    본 구문은 가축전염병 발생현황을 크롤링 하여 DataBase에 담는 용도임
    주기적으로 실행 가능해야 함.
'''

from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import pymysql
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

#웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

wd = webdriver.Chrome(ChromeDriverManager().install())

url = "https://home.kahis.go.kr/home/lkntscrinfo/selectLkntsOccrrncList.do"

diseaselist = []
farmlist = []
addrlist = []
datelist = []
animallist = []

wd.get(url=url)

# 검색기준을 만들어주려면? 아니면 다 들고와서 돼지와 소에 다같이 적용해도 됨.
# dropdown = Select(wd.find_elements(By.XPATH, '//*[@id="legalIctsdGradSe"]/option[2]'))
# select = Select(wd.find_element(By.CSS_SELECTOR, '#legalIctsdGradSe'))
# select.select_by_index(1)

# 버튼으로 다 돌아가면서 검색하게는 안되나?


# 화면내의 각 페이지 10부터 1까지 들어가는 단계
for i in range(10, 0, -1):
    wd.find_element(By.CSS_SELECTOR, f"#homeLkntscrinfoVO > table:nth-child(7) > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child({2*i + 1}) > a").click()
    
    # 테이블 내의 콘텐츠들을 담아오는 단계
    for k in range(10, 0, -1):      
        
        req = wd.page_source
        soup = BeautifulSoup(req, 'html.parser')

        # 발병일자
        date = soup.select(f'#homeLkntscrinfoVO > table:nth-child(6) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child({k}) > td:nth-child(4)')
        datelist.append(date[0].text.split(sep = "\n")[0])
        # print("1",date[0].text)
        
        # 발병농장명
        farm = soup.select(f'#homeLkntscrinfoVO > table:nth-child(6) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child({k}) > td:nth-child(2)')
        farmlist.append(farm[0].text.split(sep = "\n")[3].strip(" "))
        # print("2",farm[0].text)
        # 발병위치(주소)
        addr = soup.select(f'#homeLkntscrinfoVO > table:nth-child(6) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child({k}) > td:nth-child(3)')
        addrlist.append(addr[0].text)
        # print("3",addr[0].text)
        # 질병명
        disease = soup.select(f'#homeLkntscrinfoVO > table:nth-child(6) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child({k}) > td:nth-child(1)')
        diseaselist.append(disease[0].text)
        # print("4",disease[0].text)
        # 축종
        animal = soup.select(f'#homeLkntscrinfoVO > table:nth-child(6) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child({k}) > td:nth-child(5)')
        animallist.append(animal[0].text)
        # print("5",animal[0].text)
        # print(i, "/", disease[0].text, "/", farm[0].text.split(sep = "\n")[3].strip(" "), "/", addr[0].text, "/", date[0].text.split(sep = "\n")[0], "/", animal[0].text)
    
wd.quit()

# AI현황 정보를 데이터베이스에 저장
mydb = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '0000',
    db = 'price',
    charset='utf8'
)
cursor = mydb.cursor()

for i in range(len(datelist)):
    # print(i)
    date = datelist[i]
    ds_nm = diseaselist[i]
    farm_nm = farmlist[i]
    addr = addrlist[i]
    animal = animallist[i]

    # sql = "INSERT INTO disease_current( ds_nm, farm_nm, addr, date, animal ) VALUES (%s, %s, %s, %s, %s)"

    # 중복제거 쿼리 시도
    sql = "INSERT IGNORE INTO disease_current( date, farm_nm, addr, ds_nm, animal ) VALUES (%s, %s, %s, %s, %s)"
    # 이방법은 일단 두개 pk 조건이 and 가 아닌 or로 엮인다는 것과
    # 인덱스가 중복삭제될 시 건너뛰어진다는 단점이 있음.
    val = (date, farm_nm, addr, ds_nm, animal)

    cursor.execute(sql,val)
    mydb.commit()

mydb.close()