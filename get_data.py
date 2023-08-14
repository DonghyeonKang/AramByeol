from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess


# 크롬 디버그 모드로 실행 
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\heizl\chromeCookie"')
url = "https://www.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do"

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox') #보안 기능 비활성화(샌드박스라는 공간을 비활성화 시킴)
options.add_argument('--disable-dev-shm-usage') #/dev/shm 공유메모리 디렉토리를 사용하지 않음 
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

driver.get(url)
wait = WebDriverWait(driver, 10)  # 10초 동안 대기
aram_html = driver.page_source # 웹 페이지의 전체 HTML 소스 코드 가져오기

# soup에 넣어주기
soup = BeautifulSoup(aram_html, 'html.parser')

week = soup.find('thead')
# 월요일부터 일요일까지의 요일 텍스트 추출
day_date = week.find_all('th', scope='col')[1:]
day_date_text = [day.get_text(strip=True) for day in day_date]

#print(day_date_text) #월2023-08-14

menu = soup.find('tbody')
all_menu = menu.find_all('tr')
#print(all_menu) #아침,점심,저녁 html 리스트로 출력

#아침,점심,저녁 각각 변수에 html 저장
for i in range(3):
    if(i==0):
        mornings = all_menu[i]
    elif(i==1):
        lunches = all_menu[i]
    else:
        dinners = all_menu[i]

#print(mornings)

#아침
daily_morning = mornings.find_all('td')
morning_text = [morning.get_text(strip=True) for morning in daily_morning]
#print(morning_text) #A코스,B코스,테이크아웃 출력

#점심
daily_lunch = lunches.find_all('td')
lunch_text = [lunch.get_text(strip=True) for lunch in daily_lunch]

#저녁
daily_dinner = dinners.find_all('td')
dinner_text = [dinner.get_text(strip=True) for dinner in daily_dinner]


driver.quit()




