import pymysql
import db_auth as db_auth

class MenuRepository:
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

    def selectMenuByDay(self, day):
        self.getConnection()
        data = []
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT menu, course FROM morning WHERE day=%s", day
            )
            data.append(self.cursor.fetchall())
            self.cursor.execute(
                "SELECT menu, course FROM lunch WHERE day=%s", day
            )
            data.append(self.cursor.fetchall())
            self.cursor.execute(
                "SELECT menu, course FROM dinner WHERE day=%s", day
            )
            data.append(self.cursor.fetchall())

            self.connection.commit()
            return data
        except Exception as e:
            print(e)
            return "Error: Database Select Error"
        finally:
            self.closeConnection()