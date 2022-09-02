import pymysql.cursors
import db_auth

class MailRepository():
    def __init__(self) -> None:
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

    # user_id 와 해당 유저에게 보낸 인증 번호를 저장
    def insertNumber(self, userId, token):
        self.getConnection()
        try:
            arr = [userId, token]
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "INSERT INTO mail(user_id, token) VALUES(%s, %s)", arr, 
            )
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "Error: Database Insert Error"
        finally:
            self.closeConnection()

    def selectToken(self, userId):
        self.getConnection()
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT token FROM mail WHERE user_id=%s", userId, 
            )
            result = self.cursor.fetchall()
            if len(result) == 0:
                return "no token"
            else:
                return result[0]['token']
        except Exception as e:
            print(e)
            return "Error: Database Insert Error"
        finally:
            self.closeConnection()

    # 인증 번호 삭제
    def deleteNumber(self, userId):
        self.getConnection()
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "DELETE FROM mail WHERE user_id=%s", userId, 
            )
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "Error: Database Insert Error"
        finally:
            self.closeConnection()