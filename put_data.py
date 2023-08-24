from get_data import *
import pymysql.cursors  # python과 mysql(mariadb) 연동
import db_auth

# Connect to the DB
login = db_auth.db_login
connection = pymysql.connect(host=login['localhost'],
                             user=login['root'],
                             password=login['root0312'],
                             db=login['arambyeol'],
                             charset=login['utf8'],
                             cursorclass=pymysql.cursors.DictCursor)

#get_data 에서 스크래핑한 값들 대입
day_date = day_date
day_morning = morning
day_lunch = lunch
day_dinner = dinner



