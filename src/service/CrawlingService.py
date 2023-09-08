from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 디버그 모드로 실행 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
url = "https://www.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do"

driver.get(url)
wait = WebDriverWait(driver, 10)  # 10초 동안 대기
aram_html = driver.page_source # 웹 페이지의 전체 HTML 소스 코드 가져오기
file = open("html_code.txt","w",encoding="utf-8")
file.write(aram_html)
driver.quit()

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

# 아침 메뉴 요일별 딕셔너리 형태로 추출
morning_list = []
morning = {}

for day_morning in morning_html:
    morning_courseMenu = {}
    morning_course = day_morning.find_all('div')

    # 코스별 메뉴 딕셔너리 형태로 저장 
    for one_course in morning_course:
        try:
            course_element = one_course.find('p', class_='fm_tit_p mgt15')
            if course_element:
                course = course_element.get_text(strip=True)
            else:
                continue

            menu = one_course.find('p', class_='').get_text(separator=', ')
            morning_courseMenu[course] = menu

        # 요소를 찾지 못한 경우 예외 처리
        except AttributeError as e:
            print("morning 요소 찾지 못함")
        
    morning_list.append(morning_courseMenu)

# 요일이랑 메뉴 매칭
for i, day in enumerate(days):
    morning[day] = morning_list[i]

print("morning:",morning,"\n")


# 점심 메뉴 요일별 딕셔너리 형태로 추출
lunch_list = []
lunch = {}

for day_lunch in lunch_html:
    lunch_courseMenu = {}
    lunch_course = day_lunch.find_all('div')

    # 코스별 메뉴 딕셔너리 형태로 저장 
    for one_course in lunch_course:
        try:
            course_element = one_course.find('p', class_='fm_tit_p mgt15')
            if course_element:
                course = course_element.get_text(strip=True)
            else:
                continue

            menu = one_course.find('p', class_='').get_text(separator=', ')
            lunch_courseMenu[course] = menu

        # 요소를 찾지 못한 경우 예외 처리
        except AttributeError as e:
            print("lunch 요소 찾지 못함")
    
    lunch_list.append(lunch_courseMenu)

# 요일이랑 메뉴 매칭
for i, day in enumerate(days):
    lunch[day] = lunch_list[i]

print("lunch:",lunch,"\n")


# 저녁 메뉴 요일별 딕셔너리 형태로 추출
dinner_list = []
dinner = {}

for day_dinner in dinner_html:
    dinner_courseMenu = {}
    dinner_course = day_dinner.find_all('div')

    # 코스별 메뉴 딕셔너리 형태로 저장 
    for one_course in dinner_course:
        try:
            course_element = one_course.find('p', class_='fm_tit_p mgt15')
            if course_element:
                course = course_element.get_text(strip=True)
            else:
                continue

            menu = one_course.find('p', class_='').get_text(separator=', ')
            dinner_courseMenu[course] = menu

        # 요소를 찾지 못한 경우 예외 처리
        except AttributeError as e:
            print("dinner 요소 찾지 못함")
        
    dinner_list.append(dinner_courseMenu)

# 요일이랑 메뉴 매칭
for i, day in enumerate(days):
    dinner[day] = dinner_list[i]

print("dinner:",dinner,"\n")

# 스크래핑한 데이터 저장 --------------------
import MenuService as MenuService
menuService = MenuService.MenuService()

menuService.clearData()
menuService.weekData(day_date)
menuService.morningData(morning)
menuService.lunchData(lunch)
menuService.dinnerData(dinner)