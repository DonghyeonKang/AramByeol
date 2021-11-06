# import requests
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get('https://newgh.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

def return_data(option):
    #br태그를 공백문자로 바꾸어 준다.
    for elem in soup.find_all(["br"]):
        elem.append('\n')    
            
    table = soup('#detailForm > div > table')
    days = soup.select_one('#detailForm > div > table > thead > tr').text.strip().replace(" ", "").split('\n')
    morning = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(1)').text.strip().split('\n')
    lunch = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(2)').text.strip().split('\n')
    dinner = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(3)').text.strip().split('\n')

    def first_index_del(arg, repeat=1):   # 첫번째 인덱스를 삭제. ('아침', '점심', '저녁')
        for i in range(repeat):
            del arg[0]

    def double_quorts_del(arg):
        search = '"'
        for i, word in enumerate(arg):
            if search in word: 
                arg[i] = word.strip(search)
        return arg

    # morning = list(filter(None, morning)); # filter로 공백 없애고 list화
    # lunch = list(filter(None, lunch)); # filter로 공백 없애고 list화
    # dinner = list(filter(None, dinner)); # filter로 공백 없애고 list화
    first_index_del(days)
    first_index_del(morning,3)
    first_index_del(lunch,3)
    first_index_del(dinner,3)

    double_quorts_del(morning)
    double_quorts_del(lunch)
    double_quorts_del(dinner)

    def split_menu_data(args):
        count = 0
        day=[]
        day.append([])
        day_count = 0
        menu_count = 0
        for element in args:
            if element == '':
                count += 1
                continue
            
            if count >=5 :
                day.append([])
                day_count += 1
            count = 0
            day[day_count].append(element)
        return day

    day_morning = split_menu_data(morning)
    day_lunch = split_menu_data(lunch)
    day_dinner = split_menu_data(dinner)
    
    if option==0:
        return days
    elif option==1:
        return day_morning
    elif option==2:
        return day_lunch
    elif option==3:
        return day_dinner











