import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from config import (
    MENU_BLOCKING_PATTERNS,
    MAX_MENU_LENGTH,
    MAX_COURSE_LENGTH,
    MEAL_TYPES,
    MEAL_TYPE_MAPPING
)

load_dotenv(override=True)

def format_date(date_str: str) -> str:
    """
    날짜 문자열을 'YYYY-MM-DD' 형식으로 변환
    예: '월 2025-04-28' -> '2025-04-28'
    """
    try:
        # 요일 제거하고 날짜 부분만 추출
        date_part = date_str.split(' ')[1]
        # datetime으로 파싱하여 유효성 검사
        datetime.strptime(date_part, '%Y-%m-%d')
        return date_part
    except (IndexError, ValueError):
        print(f"Warning: Invalid date format: {date_str}")
        return date_str

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', ''),
        db=os.environ.get('MYSQL_DATABASE', 'arambyeol'),
        charset='utf8mb4'
    )

def get_or_create_menu(cursor, menu_name: str) -> int:
    """
    메뉴를 조회하거나 새로 생성하여 menu_id를 반환
    """
    # 메뉴 이름이 최대 길이를 초과하는 경우 자르기
    menu_name = menu_name[:MAX_MENU_LENGTH] if len(menu_name) > MAX_MENU_LENGTH else menu_name
    
    try:
        # 기존 메뉴 조회
        cursor.execute("SELECT menu_id FROM menu WHERE menu = %s", (menu_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        
        # 새 메뉴 생성
        cursor.execute(
            "INSERT INTO menu (menu, img_path) VALUES (%s, %s)",
            (menu_name, '')
        )
        return cursor.lastrowid
    except pymysql.Error as e:
        print(f"Error handling menu '{menu_name}': {e}")
        raise

def parse_menu_text(menu_text: str) -> List[str]:
    """
    메뉴 텍스트를 개별 메뉴 항목으로 분리
    """
    # 구분자로 사용될 수 있는 문자들
    separators = ['/', '*', ',', '♥', '+']
    
    # [공지] 텍스트 제거
    if '[공지]' in menu_text:
        menu_text = menu_text.split('[공지]')[0].strip()
    
    # 초기 메뉴 항목 분리
    items = [item.strip() for item in menu_text.split('\n')]
    
    # 추가 구분자로 분리
    final_items = []
    for item in items:
        for sep in separators:
            if sep in item:
                # 구분자로 분리하고 각 항목 추가
                sub_items = [sub.strip() for sub in item.split(sep)]
                final_items.extend(sub_items)
                break
        else:
            # 구분자가 없는 경우 그대로 추가
            final_items.append(item)
    
    # 빈 항목 제거하고 중복 제거
    return list(set(item for item in final_items if item and len(item) > 1))

def save_menu(menu_data: Dict[str, List[Tuple[str, str, List[str]]]]):
    """
    메뉴 데이터를 DB에 저장하는 함수
    Args:
        menu_data: {
            날짜: [(식사타입, 코스명, [메뉴항목들]), ...]
        }
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # menu 테이블에 메뉴 저장
            for date, meals in menu_data.items():
                formatted_date = format_date(date)
                
                # 해당 날짜의 기존 plan 조회
                cursor.execute("""
                    SELECT p.plan_id, p.menu_id, m.menu, p.course, p.meal_type
                    FROM plan p 
                    JOIN menu m ON p.menu_id = m.menu_id 
                    WHERE p.date = %s
                """, (formatted_date,))
                existing_plans = cursor.fetchall()
                
                # 기존 plan을 dictionary로 변환 (course, menu, meal_type를 key로 사용)
                existing_plan_dict = {
                    (plan[3], plan[2], plan[4]): plan[0]  # (course, menu, meal_type): plan_id
                    for plan in existing_plans
                }
                
                # 새로운 메뉴 항목들을 저장할 set
                new_menu_items = set()
                
                # 새로운 메뉴 데이터 처리
                for meal_type, course, items in meals:
                    course = course[:MAX_COURSE_LENGTH]
                    eng_meal_type = MEAL_TYPE_MAPPING[meal_type]
                    
                    for item in items:
                        try:
                            # 메뉴 저장 또는 조회
                            menu_id = get_or_create_menu(cursor, item)
                            new_menu_items.add((course, item, eng_meal_type))
                            
                            # 이 메뉴가 기존에 없었다면 추가
                            if (course, item, eng_meal_type) not in existing_plan_dict:
                                cursor.execute(
                                    "INSERT INTO plan (menu_id, date, course, meal_type) VALUES (%s, %s, %s, %s)",
                                    (menu_id, formatted_date, course, eng_meal_type)
                                )
                                print(f"Added new menu item: {item} for {eng_meal_type} course {course}")
                        except Exception as e:
                            print(f"Error processing menu item '{item}': {e}")
                            continue
                
                # 기존 메뉴 중 새로운 메뉴에 없는 항목 삭제
                for (course, menu, meal_type), plan_id in existing_plan_dict.items():
                    if (course, menu, meal_type) not in new_menu_items:
                        cursor.execute("DELETE FROM plan WHERE plan_id = %s", (plan_id,))
                        print(f"Removed outdated menu item: {menu} from {meal_type} course {course}")
            
            conn.commit()
            print("Successfully updated menu data in database")
            
    except Exception as e:
        print(f"Error saving menu data: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

def fetch_menu_page():
    # Target URL
    url = "https://www.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do"
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Send GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Create a directory for storing HTML files if it doesn't exist
        os.makedirs('html_files', exist_ok=True)
        
        # Use fixed filename
        filename = 'html_files/menu.html'
        
        # Save the HTML content
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"Successfully saved HTML content to {filename}")
        return True
        
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return False

def parse_menu():
    try:
        with open('html_files/menu.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the table containing menu information
        table = soup.find('table')
        if not table:
            print("Could not find menu table")
            return
        
        # Get dates from table headers
        headers = table.find_all('th')
        dates = [header.text.strip() for header in headers[1:]]  # Skip first header (구분)
        
        # Dictionary to store all menu data
        menu_data = {}
        
        # Get menu rows
        rows = table.find_all('tr')
        
        # Process each meal type (아침, 점심, 저녁)
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if not cells:
                continue
                
            meal_type = cells[0].text.strip()  # 아침, 점심, 저녁
            if meal_type not in MEAL_TYPES:
                continue
                
            print(f"\n=== {meal_type} ===")
            
            # Process each day's menu
            for date, cell in zip(dates, cells[1:]):
                if date not in menu_data:
                    menu_data[date] = []
                
                print(f"\n[{date}]")
                
                # Find all menu sections in the cell
                menu_sections = cell.find_all('div')
                for section in menu_sections:
                    # Get course title
                    title = section.find('p', class_='fm_tit_p')
                    if not title:
                        continue
                        
                    course_title = title.text.strip()
                    print(f"\n{course_title}")
                    
                    # Get menu items
                    menu_items = []
                    menu_p = section.find('p', class_='')  # Find the p tag containing menu items
                    if menu_p:
                        # Get the raw text content
                        menu_text = menu_p.get_text('\n')  # Use \n as separator for <br> tags
                        
                        # Split into lines and process each line
                        items = menu_text.split('\n')
                        
                        # Filter out notices and empty lines
                        for item in items:
                            item = item.strip()
                            # Skip empty items and blocked items
                            if item and not any(pattern in item for pattern in MENU_BLOCKING_PATTERNS):
                                menu_items.append(item)
                                print(f"- {item}")
                    
                    if menu_items:
                        # Store menu data
                        menu_data[date].append((meal_type, course_title[:MAX_COURSE_LENGTH], menu_items))

        # Save menu data to database
        save_menu(menu_data)

    except FileNotFoundError:
        print("Menu HTML file not found. Please run fetch_menu_page() first.")
    except Exception as e:
        print(f"Error parsing menu: {e}")

if __name__ == "__main__":
    fetch_menu_page()
    parse_menu()