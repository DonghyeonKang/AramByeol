import pymysql
from flask_login import UserMixin
from db import *
import bcrypt

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='111111', database='arambyeol')
cursor = db.cursor()    # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

# 회원가입
def useradd(id, pw):
    sql = "INSERT INTO users(user_id, user_pw) VALUES ('%s', '%s');" % (id, pw)
    cursor.execute(sql)
    db.commit()

# users table 조회.  있으면 true 없으면 false
def check_userId(userid):
    sql = 'SELECT user_id FROM users WHERE user_id="%s"' % userid
    cursor.execute(sql)
    db.commit()
    answer = cursor.fetchall()
    if(len(answer) == 0):
        return False
    else:
        return True

def login_check(input_username, input_password):
    # bcrypt hash transfer
    input_password = input_password.encode('UTF-8')
    # MySQL DB에 해당 계정 정보가 있는지 확인
    cursor.execute('SELECT * FROM users WHERE user_id = %s', [input_username])
    # 값이 유무 확인 결과값 account 변수로 넣기
    account = cursor.fetchone()
    # DB에 계정 정보가 없으면 account == None
    if account == None:
        return False
    check_password = bcrypt.checkpw(input_password, account[2].encode('utf-8'))
    return check_password