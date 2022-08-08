import pymysql.cursors  # python과 mysql(mariadb) 연동
import db_auth

class postingRepository:
    def __init__(self) -> None:
        # Connect to the DB
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

    def insertPosting(self, data):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "INSERT INTO post(user_id, title, content, date, category, score, meal_time, image) values(%s, %s, %s, %s, %s, %d, %s, %s))", data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]
            )
    
            self.connection.commit()  # 실행한 문장들 적용
            return 'success'
        except:
            return "Error: Database Insert Error"
    

    
    