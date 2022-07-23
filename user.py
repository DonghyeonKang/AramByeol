import pymysql
import bcrypt
import db_auth


login = db_auth.db_login
def db_connection():
    login = db_auth.db_login
    connection = pymysql.connect(host=login['host'],
                            user=login['user'],
                            password=login['password'],
                            db=login['db'],
                            charset=login['charset'],
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

# 회원가입
def useradd(id, pw):
    connection = db_connection() # db 연결
    cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
    sql = "INSERT INTO users(user_id, user_pw) VALUES ('%s', '%s')" % (id,pw)  # 쿼리문 작성
    cursor.execute(sql) # 쿼리 실행 
    connection.commit() # 쿼리 적용
    connection.close() # db 연결해제

# 아이디가 존재하는 지 체크함
def check_userId(userid):
    connection = db_connection() # db 연결
    cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
    sql = 'SELECT user_id FROM users WHERE user_id="%s"' % userid # 쿼리문 작성
    cursor.execute(sql) # 쿼리 실행
    answer = cursor.fetchall() # 받아온 모든 데이터를 가져옴
    connection.close()  # db 해제
    if(len(answer) == 0): # 가져온 데이터가 없다면 false 있다면 true
        return False
    else:
        return True

# 비밀 번호를 비교함
def check_userPassword(input_username, input_password):
    connection = db_connection() # DB 연결
    cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
    input_password = input_password.encode('utf-8') # bcrypt hash transfer
    cursor.execute('SELECT * FROM users WHERE user_id = %s', [input_username]) # MySQL DB에 해당 계정 정보가 있는지 확인
    account = cursor.fetchone() # 값이 유무 확인 결과값 account 변수로 넣기
    connection.close() # DB 해제
    
    if account == None: # DB에 계정 정보가 없으면 account == None
        return False
    else:
        check_password = bcrypt.checkpw(input_password, account['user_pw'].encode('utf-8')) # 해싱된 비밀번호 비교
        return check_password   # 일치하면 true, 틀리면 false
