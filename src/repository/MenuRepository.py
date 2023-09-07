from service.CrawlingService import *
import db_auth
import pymysql.cursors  # python과 mysql(mariadb) 연동
## 일주일에 한 번 씩 실행될 것임. ##

class MenuRepository:
    # db 연결
    def db_connection(self):
        login = db_auth.db_login
        connection = pymysql.connect(host=login['host'],
                                user=login['user'],
                                password=login['password'],
                                db=login['db'],
                                charset=login['charset'],
                                cursorclass=pymysql.cursors.DictCursor)
        return connection
    
    # 이미 있는 테이블이면 지우고 다시 생성하는 query문
    def db_update(self):  
        connection = self.db_connection() # db 연결
        cursor = connection.cursor() # SQL 문장을 DB 서버에 전송하기 위한 객체

        if cursor.execute("SHOW TABLES LIKE %s", 'week') or cursor.execute("SHOW TABLES LIKE %s", 'morning') or cursor.execute("SHOW TABLES LIKE %s", 'lunch') or cursor.execute("SHOW TABLES LIKE %s", 'dinner'):
            cursor.execute("DROP TABLE week")
            cursor.execute("DROP TABLE morning")
            cursor.execute("DROP TABLE lunch")
            cursor.execute("DROP TABLE dinner")

        cursor.execute(
            "CREATE TABLE week(day VARCHAR(2) NOT NULL primary key,date VARCHAR(11) NOT NULL)")
        cursor.execute(
            "CREATE TABLE morning(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(100) NOT NULL)")
        cursor.execute(
            "CREATE TABLE lunch(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(100) NOT NULL)")
        cursor.execute(
            "CREATE TABLE dinner(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(100) NOT NULL)")
        connection.commit() # 쿼리 적용
        connection.close() # db 연결해제


    # week 테이블에 day,date 값 넣는 query문 반환 함수
    def db_week():
        week_sql = "INSERT INTO week (day, date) VALUES (%s, %s)"

        return week_sql


    # morning 테이블 대입 query문 반환 함수
    def db_morning():
        morning_sql = "INSERT INTO morning (day, course, menu) VALUES (%s,%s,%s)"

        return morning_sql
    

    # lunch 테이블 대입 query문 반환 함수
    def db_lunch():
        lunch_sql = "INSERT INTO lunch (day, course, menu) VALUES (%s,%s,%s)"

        return lunch_sql
    
    # dinner 테이블 대입 query문 반환 함수
    def db_dinner():
        dinner_sql = "INSERT INTO dinner (day, course, menu) VALUES (%s,%s,%s)"

        return dinner_sql

