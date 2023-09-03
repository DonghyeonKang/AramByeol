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
date_query = "SELECT date FROM week WHERE date = %s"

# 딕셔너리 첫번째 값 가져오기(값이 없다면 none 반환)
first_dateValue = next(iter(day_date.values()), None)

# # 테이블에 같은 날짜 값이 존재하는지 확인
# if first_dateValue is not None:
#     cursor.execute(date_query,(first_dateValue))
#     result = cursor.fetchone()

#     # 값이 없다면 테이블에 값 넣기
#     if result == None:
#         for day, date in day_date.items():
#             cursor.execute(week_sql, (day, date))

def db_update():  # 이미 있는 테이블이면 지우고 다시 생성 
        if cursor.execute("SHOW TABLES LIKE %s", 'week') or cursor.execute("SHOW TABLES LIKE %s", 'morning') or cursor.execute("SHOW TABLES LIKE %s", 'lunch') or cursor.execute("SHOW TABLES LIKE %s", 'dinner'):
            cursor.execute("DROP TABLE week")
            cursor.execute("DROP TABLE morning")
            cursor.execute("DROP TABLE lunch")
            cursor.execute("DROP TABLE dinner")

        cursor.execute(
            "CREATE TABLE week(day VARCHAR(2) NOT NULL primary key,date VARCHAR(11) NOT NULL)")
        cursor.execute(
            "CREATE TABLE morning(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(50) NOT NULL)")
        cursor.execute(
            "CREATE TABLE lunch(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(50) NOT NULL)")
        cursor.execute(
            "CREATE TABLE dinner(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(50) NOT NULL)")
        

# week 테이블에 day, date 값 넣기
db_update()
for day, date in day_date.items():
    cursor.execute(week_sql, (day, date))


# morning 테이블에 day,cource,menu 값 넣기
morning_sql = "INSERT INTO morning (day, course, menu) VALUES (%s,%s,%s)"

for day, course_data in day_morning.items():
    morning_course = course_data
    for course, menu in morning_course.items():
        cursor.execute(morning_sql,(day, course, menu))


# lunch 테이블에 day,cource,menu 값 넣기
lunch_sql = "INSERT INTO lunch (day, course, menu) VALUES (%s,%s,%s)"

for day, course_data in day_lunch.items():
    lunch_course = course_data
    for course, menu in lunch_course.items():
        cursor.execute(lunch_sql,(day, course, menu))


# dinner 테이블에 day,cource,menu 값 넣기
dinner_sql = "INSERT INTO dinner (day, course, menu) VALUES (%s,%s,%s)"

for day, course_data in day_dinner.items():
    dinner_course = course_data
    for course, menu in dinner_course.items():
        cursor.execute(dinner_sql,(day, course, menu))






connection.commit()
connection.close()