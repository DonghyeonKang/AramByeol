import pymysql
import bcrypt
import db_auth

login = db_auth.db_login
#db = pymysql.connect(host=db_login['host'], port=db_login['port'], user=db_login['user'], passwd=db_login['password'], database=db_login['db'])
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
    connection = db_connection()
    cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
    sql = "INSERT INTO users(user_id, user_pw) VALUES ('%s', '%s')" % (id,pw)    
    cursor.execute(sql)
    connection.commit()
    connection.close()

# users table 조회.  있으면 true 없으면 false
def check_userId(userid):
    connection = db_connection()
    cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
    sql = 'SELECT user_id FROM users WHERE user_id="%s"' % userid
    cursor.execute(sql)
    connection.commit()
    answer = cursor.fetchall()
    connection.close()
    if(len(answer) == 0):   
        return False
    else:
        return True

def login_check(input_username, input_password):
    connection = db_connection()
    cursor = connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
    # bcrypt hash transfer
    input_password = input_password.encode('utf-8')
    # MySQL DB에 해당 계정 정보가 있는지 확인
    cursor.execute('SELECT * FROM users WHERE user_id = %s', [input_username])
    # 값이 유무 확인 결과값 account 변수로 넣기
    account = cursor.fetchone()
    connection.close()
    # DB에 계정 정보가 없으면 account == None
    if account == None:
        return False
    check_password = bcrypt.checkpw(input_password, account['user_pw'].encode('utf-8'))
    return check_password
