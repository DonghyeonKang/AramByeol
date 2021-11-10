import pymysql
from flask_login import UserMixin
from db import *

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='111111', database='arambyeoldb')
cursor = db.cursor()    # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

# 회원가입
def useradd(id, pw):
    sql = "INSERT INTO users(id, password) VALUES ('%s', '%s');" % (id, pw)
    cursor.execute(sql)
    db.commit()

# users table 조회.  있으면 true 없으면 false
def check_userId(userid):
    sql = 'SELECT id FROM users WHERE id="%s"' % userid
    cursor.execute(sql)
    db.commit()
    answer = cursor.fetchall()
    
    if(len(answer) == 0):
        return True
    else:
        return False
