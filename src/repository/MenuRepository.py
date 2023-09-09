import repository.db_auth as db_auth
import pymysql.cursors  # python과 mysql(mariadb) 연동
## 일주일에 한 번 씩 실행될 것임. ##

class MenuRepository:
    def __init__(self) -> None:
        self.login = db_auth.db_login

    def getConnection(self):
        self.connection = pymysql.connect(host=self.login['host'],
                                     user=self.login['user'],
                                     password=self.login['password'],
                                     db=self.login['db'],
                                     charset=self.login['charset'],
                                     cursorclass=pymysql.cursors.DictCursor)

    def closeConnection(self):
        self.connection.close()

    # 이미 있는 테이블이면 지우고 다시 생성하는 query문
    def db_update(self):  
        connection = self.getConnection() # db 연결
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
    def db_week(self, day, date):
        connection = self.getConnection() # db 연결
        cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        week_sql = "INSERT INTO week (day, date) VALUES ('%s', '%s')" % (day, date)

        cursor.execute(week_sql) # 쿼리 실행 
        connection.commit() # 쿼리 적용
        connection.close() # db 연결해제


    # morning 테이블 대입 query문 반환 함수
    def db_morning(self, day, course, menu):
        connection = self.getConnection() # db 연결
        cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
    
        morning_sql = "INSERT INTO morning (day, course, menu) VALUES ('%s', '%s', '%s')" % (day, course, menu)

        cursor.execute(morning_sql) # 쿼리 실행 
        connection.commit() # 쿼리 적용
        connection.close() # db 연결해제
    

    # lunch 테이블 대입 query문 반환 함수
    def db_lunch(self, day, course, menu):
        connection = self.getConnection() # db 연결
        cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        lunch_sql = "INSERT INTO lunch (day, course, menu) VALUES ('%s', '%s', '%s')" % (day, course, menu)

        cursor.execute(lunch_sql) # 쿼리 실행 
        connection.commit() # 쿼리 적용
        connection.close() # db 연결해제
    
    # dinner 테이블 대입 query문 반환 함수
    def db_dinner(self, day, course, menu):
        connection = self.getConnection() # db 연결
        cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        dinner_sql = "INSERT INTO dinner (day, course, menu) VALUES ('%s', '%s', '%s')" % (day, course, menu)

        cursor.execute(dinner_sql) # 쿼리 실행 
        connection.commit() # 쿼리 적용
        connection.close() # db 연결해제

    def selectMenuByDay(self, day):
            self.getConnection()
            data = []
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(
                    "SELECT menu, course FROM morning WHERE day=%s", day
                )
                data.append(self.cursor.fetchall())
                self.cursor.execute(
                    "SELECT menu, course FROM lunch WHERE day=%s", day
                )
                data.append(self.cursor.fetchall())
                self.cursor.execute(
                    "SELECT menu, course FROM dinner WHERE day=%s", day
                )
                data.append(self.cursor.fetchall())

                self.connection.commit()
                return data
            except Exception as e:
                print(e)
                return "Error: Database Select Error"
            finally:
                self.closeConnection()