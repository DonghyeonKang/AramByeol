import db_auth
import pymysql


class UserRepository:
    def db_connection(self):
        login = db_auth.db_login
        connection = pymysql.connect(host=login['host'],
                                user=login['user'],
                                password=login['password'],
                                db=login['db'],
                                charset=login['charset'],
                                cursorclass=pymysql.cursors.DictCursor)
        return connection

    # 회원가입
    def useradd(self,id, pw):
        connection = self.db_connection() # db 연결
        cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
        sql = "INSERT INTO users(user_id, user_pw) VALUES ('%s', '%s')" % (id,pw)  # 쿼리문 작성
        cursor.execute(sql) # 쿼리 실행 
        connection.commit() # 쿼리 적용
        connection.close() # db 연결해제

    # 아이디를 조회한다. 
    def findUserIdByUserId(self, userid):
        connection = self.db_connection() # db 연결
        cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        sql = 'SELECT user_id FROM users WHERE user_id="%s"' % userid # 쿼리문 작성
        cursor.execute(sql) # 쿼리 실행
        answer = cursor.fetchall() # 받아온 모든 데이터를 가져옴
        connection.close()  # db 해제

        return answer
        
    # 사용자 계정을 조회한다. 
    def findByUserId(self, input_username):
        connection = self.db_connection() # DB 연결
        cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
        
        cursor.execute('SELECT user_pw FROM users WHERE user_id = %s', [input_username]) # MySQL DB에 해당 계정 정보가 있는지 확인
        password = cursor.fetchone() # 값이 유무 확인 결과값 account 변수로 넣기
        connection.close() # DB 해제

        return password
        
        
