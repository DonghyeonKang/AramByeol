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

cursor = connection.cursor()

# week 테이블에 day,date 값 넣는 query문
week_sql = "INSERT INTO week (day, date) VALUES (%s, %s)"

# 테이블에 중복 데이터 확인하는 query문
date_query = "SELECT date FROM week WHERE date = %s"


def db_update():  # 이미 있는 테이블이면 지우고 다시 생성하는 query문
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


# morning 테이블 대입 query문
morning_sql = "INSERT INTO morning (day, course, menu) VALUES (%s,%s,%s)"

# lunch 테이블 대입 query문
lunch_sql = "INSERT INTO lunch (day, course, menu) VALUES (%s,%s,%s)"

# dinner 테이블 대입 query문
dinner_sql = "INSERT INTO dinner (day, course, menu) VALUES (%s,%s,%s)"

