from bs4 import BeautifulSoup   # selenium으로 스크래핑한 것을 1차 가공
from selenium import webdriver  # google webdriver를 사용할거임
from pyvirtualdisplay import Display # 가상 디스플레이
import subprocess   # OS 명령어 연동
from webdriver_manager.chrome import ChromeDriverManager

import scrap_service as scrapService
import scrap_repo as scrapRepo 

# TODO 여기 자동화할 필요 있음
if 1 == 0:
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get('https://www.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do') # 스크래핑할 동적 웹사이트 주소
    html = driver.page_source   # 드라이버로 긁어온 정보를 html에 담음
    driver.close()
    display.stop()
    subprocess.call("pkill -9 chrome", shell=True) # chrome driver 제대로 안꺼지면 꺼야함
    # 스크래핑한 데이터 임시 저장. 로직 에러시 재스크래핑 방지
    with open("tmpScrap.txt", "w") as file:
        file.write(html)
        file.close()
else:
    with open("tmpScrap.txt", "r") as file:
        html = file.read()
        file.close()

# -------------------------------------------------------------------
courseList = ['A', 'B', 'C', '테이크아웃', 'T/O', '한식', '일품', 'A코스', 'B코스', 'C코스', '베이커리', '죽',
                  'A코스/한식', 'B코스/베이커리', 'C코스/죽', '◆공지◆', 'B코스/일품', '공지']   # 새로운 코스 등장하면 여기에 추가!

# 객체 생성
scrapRepo = scrapRepo.ScrappingRepository(courseList)

# -------------------------------------------------------------------

soup = BeautifulSoup(html, 'html.parser') # Beautifulsoup로 1차 가공
#br태그를 공백문자로 바꾸어 준다.
for elem in soup.find_all(["br"]):
    elem.append('\n')

# days : 날짜 및 요일, morning : 아침, lunch : 점심, dinner : 저녁
try:
    days = soup.select_one('#detailForm > div > table > thead > tr').text.strip().replace(" ", "").split('\n')      # NoneType 이면 IP 차단 되었을 가능성 있음
    morning = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(1)').text.strip().split('\n')
    lunch = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(2)').text.strip().split('\n')
    dinner = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(3)').text.strip().split('\n')
except Exception as e:  # 데이터를 가져옴에 있어서 에러가 발생한다면, 에러 내용을 slack으로 전송
    print(e)
    #sendData(str(e))

# -------------------------------------------------------- get Data ----------------------------------------------------------------
# 식사 타입이 들어간('아침', '점심', '저녁') 첫번째 인덱스를 제거
scrapService.first_index_del(days)
if len(morning) > 1:
    scrapService.first_index_del(morning,3)
else:
    scrapService.first_index_del(morning,1)

if len(lunch) > 1:
    scrapService.first_index_del(lunch,3)
else:
    scrapService.first_index_del(lunch,1)

if len(dinner) > 1:
    scrapService.first_index_del(dinner,3)
else:
    scrapService.first_index_del(dinner,1)

# 따옴표 제거
scrapService.double_quorts_del(morning)
scrapService.double_quorts_del(lunch)
scrapService.double_quorts_del(dinner)

# 필요없는 텍스트 제거
morning = scrapService.data_blocking(morning)
lunch = scrapService.data_blocking(lunch)
dinner = scrapService.data_blocking(dinner)

# 요일별로 데이터를 나눔
day_mornings = scrapService.split_menu_data(morning)
day_lunches = scrapService.split_menu_data(lunch)
day_dinners = scrapService.split_menu_data(dinner)
# ---------------------------------------------------------------- db.py --------------------------------------------------------------
# week, morning, lunch, dinner 테이블 데이터 비우기
scrapRepo.initaializeDB()

# week 테이블에 데이터 저장
scrapRepo.week_update(days)
import copy
# 메뉴들을 메뉴 데이터베이스에 저장함
day_morning = copy.deepcopy(day_mornings)
day_lunch = copy.deepcopy(day_lunches)
day_dinner = copy.deepcopy(day_dinners)
menuData = scrapService.mergeMeals(day_morning, day_lunch, day_dinner, courseList)
scrapRepo.update_menudata(menuData)

# 주간 아침 점심 저녁 데이터 저장
scrapRepo.update_week_menu(day_mornings, 0)
scrapRepo.update_week_menu(day_lunches, 1)
scrapRepo.update_week_menu(day_dinners, 2)

# 객체 삭제
del scrapRepo