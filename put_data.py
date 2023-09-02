from get_data import *
import pymysql.cursors  # python과 mysql(mariadb) 연동
## 일주일에 한 번 씩 실행될 것임. ##

# Connect to the DB
connection = pymysql.connect(host='localhost',  # 호스트 주소
                             user='root',       # 사용자 이름
                             password='root0312',  # 비밀번호
                             db='arambyeol',    # 데이터베이스 이름
                             charset='utf8',    # 문자 인코딩
                             cursorclass=pymysql.cursors.DictCursor)  # 커서 클래스 설정

#get_data 에서 스크래핑한 값들 대입
day_date = day_date
day_morning = morning
day_lunch = lunch
day_dinner = dinner

cursor = connection.cursor()

# week 테이블에 day,date 값 넣기
week_sql = "INSERT INTO week (day, date) VALUES (%s, %s)"

for day, date in day_date.items():
    cursor.execute(week_sql, (day, date))

# morning 테이블에 day,cource,menu 값 넣기
morning_sql = "INSERT INTO morning (day, cource, menu) VALUES (%s, %s, %s)"



connection.commit()
connection.close()