from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess


# 크롬 디버그 모드로 실행 
# subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\heizl\chromeCookie"')
# url = "https://www.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do"

# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox') #보안 기능 비활성화(샌드박스라는 공간을 비활성화 시킴)
# options.add_argument('--disable-dev-shm-usage') #/dev/shm 공유메모리 디렉토리를 사용하지 않음 
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# driver = webdriver.Chrome(options=options)

# driver.get(url)
# wait = WebDriverWait(driver, 10)  # 10초 동안 대기
# aram_html = driver.page_source # 웹 페이지의 전체 HTML 소스 코드 가져오기
#file = open("html_code.txt","w",encoding="utf-8")
#file.write(aram_html)
# driver.quit()
# subprocess.call("pkill -9 chrome", shell=True) # chrome driver 제대로 안꺼지면 꺼야함


aram_html = open('html_code.txt','rt',encoding='utf-8').read()
# soup에 넣어주기
soup = BeautifulSoup(aram_html, 'html.parser')

# 날짜 정보 추출 및 딕셔너리로 변환
day_date = {}
days = ['월', '화', '수', '목', '금', '토', '일']

th_tags = soup.find_all('th')  # <th> 태그 찾기

for th_tag in th_tags[1:8]:
    day = th_tag.contents[0]  # 요일 
    date = th_tag.find('br').next_sibling  # <br> 태그 다음 텍스트 노드 추출
    if date is not None:
        date = date.strip()
        day_date[day] = date

menu_html = soup.find('tbody')
all_menulist = menu_html.find_all('tr')

morning_html = all_menulist[0].find_all('td')
lunch_html = all_menulist[1].find_all('td')
dinner_html = all_menulist[2].find_all('td')


#일주일치 요일별 아침 메뉴 
morning = {}
morning_courseMenu = {}

for day_morning in morning_html:
    morning_course = day_morning.find_all('div')

    for one_course in morning_course:
        course = one_course.find('p', class_='fm_tit_p mgt15').get_text(strip=True)
        menu = one_course.find('p', class_='').get_text('\n')
        morning_courseMenu[course] = menu
    
    for day in days:
        morning[day] = morning_courseMenu

print("아침:",morning,"\n") 


#일주일치 요일별 점심 메뉴 
lunch = {}
lunch_courseMenu = {}

for day_lunch in lunch_html:
    lunch_course = day_lunch.find_all('div')

    for one_course in lunch_course:
        course = one_course.find('p', class_='fm_tit_p mgt15').get_text(strip=True)
        menu = one_course.find('p', class_='').get_text('\n')
        lunch_courseMenu[course] = menu
    
    for day in days:
        lunch[day] = lunch_courseMenu

print("점심:",lunch, "\n") 

#일주일치 요일별 저녁 메뉴 
dinner = {}
dinner_courseMenu = {}

for day_dinner in dinner_html:
    dinner_course = day_dinner.find_all('div')

    for one_course in dinner_course:
        course = one_course.find('p', class_='fm_tit_p mgt15').get_text(strip=True)
        menu = one_course.find('p', class_='').get_text('\n')
        dinner_courseMenu[course] = menu
    
    for day in days:
        dinner[day] = dinner_courseMenu

print("저녁:",dinner) 








