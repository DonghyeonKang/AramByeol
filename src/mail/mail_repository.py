import pymysql.cursors
import db_auth

class MailRepository():
    def __init__(self) -> None:
        pass

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
    def insertAuthenticationNumber(self, user_id, number):
        pass

    # 인증 번호 비교
    def checkAuthenticationNumber(self, user_id, number):
        pass

    # 인증 번호 삭제
    def deleteAuthenticationNumber(self, number):
        pass