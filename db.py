import pymysql
from db import *

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='111111')
cursor = db.cursor()    # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

# select
# insert
# delete