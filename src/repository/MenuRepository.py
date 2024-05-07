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
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        if cursor.execute("SHOW TABLES LIKE %s", 'week') or cursor.execute("SHOW TABLES LIKE %s", 'morning') or cursor.execute("SHOW TABLES LIKE %s", 'lunch') or cursor.execute("SHOW TABLES LIKE %s", 'dinner'):
            cursor.execute("DROP TABLE week")
            cursor.execute("DROP TABLE morning")
            cursor.execute("DROP TABLE lunch")
            cursor.execute("DROP TABLE dinner")

        cursor.execute(
            "CREATE TABLE week(day VARCHAR(2) NOT NULL primary key,date VARCHAR(11) NOT NULL)")
        cursor.execute(
            "CREATE TABLE morning(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu text NOT NULL)")
        cursor.execute(
            "CREATE TABLE lunch(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu text NOT NULL)")
        cursor.execute(
            "CREATE TABLE dinner(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu text NOT NULL)")
        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제


    # week 테이블에 day,date 값 넣는 query문 반환 함수
    def db_week(self, day, date):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        week_sql = "INSERT INTO week (day, date) VALUES ('%s', '%s')" % (day, date)

        cursor.execute(week_sql) # 쿼리 실행 
        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제


    # morning 테이블 대입 query문 반환 함수
    def db_morning(self, day, course, menu):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
    
        morning_sql = "INSERT INTO morning (day, course, menu) VALUES ('%s', '%s', '%s')" % (day, course, menu)

        cursor.execute(morning_sql) # 쿼리 실행 
        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제
    

    # lunch 테이블 대입 query문 반환 함수
    def db_lunch(self, day, course, menu):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        lunch_sql = "INSERT INTO lunch (day, course, menu) VALUES ('%s', '%s', '%s')" % (day, course, menu)

        cursor.execute(lunch_sql) # 쿼리 실행 
        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제
    
    # dinner 테이블 대입 query문 반환 함수
    def db_dinner(self, day, course, menu):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        dinner_sql = "INSERT INTO dinner (day, course, menu) VALUES ('%s', '%s', '%s')" % (day, course, menu)

        cursor.execute(dinner_sql) # 쿼리 실행 
        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제

    def insertMenuData(self, menuData):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        dinner_sql = "INSERT INTO menudata (menu) VALUES ('%s')" % (menuData)
        cursor.execute(dinner_sql) # 쿼리 실행 
        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제

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
    
    def selectWeekData(self):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        sql = "select * from week" # week 테이블의 모든 데이터
        cursor.execute(sql)
        result = cursor.fetchall()

        self.closeConnection()
        return result
    
    def selectMorning(self):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        sql = "select * from morning"
        cursor.execute(sql)
        result = cursor.fetchall()

        self.closeConnection()
        return result
    
    def selectLunch(self):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        sql = "select * from lunch"
        cursor.execute(sql)
        result = cursor.fetchall()

        self.closeConnection()
        return result

    def selectDinner(self):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        sql = "select * from dinner"
        cursor.execute(sql)
        result = cursor.fetchall()

        self.closeConnection()
        return result
    
    def selectMenuData(self, menu):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        cursor.execute("SELECT * from menudata where menu=%s", menu)
        result = cursor.fetchone()

        self.closeConnection()
        return result

    def selectMenuScore(self, menuName):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        cursor.execute("SELECT score from menudata where menu=%s", menuName)
        result = cursor.fetchall()

        self.closeConnection()
        return result

    def updateMenuScore(self, menu, reviewCount, score):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
        
        sql = "UPDATE menudata SET score='%s', reviewcount='%s' WHERE menu='%s'" % (score, reviewCount, menu)   
        print(sql)     
        cursor.execute(sql)
        self.connection.commit() # 쿼리 적용
        result = cursor.fetchone()

        self.closeConnection()
        return result