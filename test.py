from bs4 import BeautifulSoup   # selenium으로 스크래핑한 것을 1차 가공
from selenium import webdriver  # google webdriver를 사용할거임
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1920, 1080))
display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("--single-process")
chrome_options.add_argument('--disable-dev-shm-usage')
path='/root/Downloads/chromedriver'
driver = webdriver.Chrome(path, chrome_options=chrome_options)
driver.get('https://www.naver.com') # 스크래핑할 동적 웹사이트 주소
#driver.get('https://newgh.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do') # 스크래핑할 동적 웹사이트 주소

html = driver.page_source   # 드라이버로 긁어온 정보를 html에 담음
soup = BeautifulSoup(html, 'html.parser') # Beautifulsoup로 1차 가공
driver.close()
display.stop()
print(soup)
