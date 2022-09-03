import pymysql.cursors  # python과 mysql(mariadb) 연동
import src.security.db_auth as db_auth

class PostingRepository:
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
        self.getConnection()
        
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "INSERT INTO post(uid, title, content, date, score, meal_time, image) values(%s, %s, %s, %s, %s, %s, %s)", data
            )
    
            self.connection.commit()  # 실행한 문장들 적용
            return 'success'
        except Exception as e:
            print(e)
            return "Error: Database Insert Error"
        finally:
            self.closeConnection()
    
    def selectPosting(self, post_id):
        self.getConnection()

        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT * FROM post WHERE post_id = %s", post_id
            )
            result = self.cursor.fetchall()
            return result[0]
        except:
            pass
        finally:
            self.closeConnection()
        
    def updatePosting(self, post_id, data):
        self.getConnection()

        try:
            pass
        except:
            pass
        finally:
            self.closeConnection()

    def deletePosting(self, post_id):
        self.getConnection()

        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "DELETE FROM post WHERE post_id = %s", post_id
            )
            self.connection.commit()  # 실행한 문장들 적용
            return "success"
        except:
            pass
        finally:
            self.closeConnection()
    
    def getImagePath(self, post_id):
        self.getConnection()

        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT image FROM post WHERE post_id = %s", post_id
            )
            result = self.cursor.fetchall()
            return result[0]['image']
        except:
            pass
        finally:
            self.closeConnection()