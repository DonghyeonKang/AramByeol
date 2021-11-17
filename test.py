import pymysql.cursors
from db_auth import db_login

db_info = db_login
print(db_info['password'])
connection = pymysql.connect(host=db_info['host'],
                            user=db_info['user'],
                            password=db_info['password'],
                            db=db_info['db'],
                            charset=db_info['charset'],
                            cursorclass=pymysql.cursors.DictCursor
                            )
cursor = connection.cursor()
cursor.execute("SELECT * FROM menudata")
print(cursor.fetchall())