import pymysql.cursors
import db_auth

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

    #TODO 쿼리 개선 해야함
    def selectMenu(self):
        self.getConnection()
        data = []
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT * FROM morning"
            )
            data.append(self.cursor.fetchall())
            self.cursor.execute(
                "SELECT * FROM lunch"
            )
            data.append(self.cursor.fetchall())
            self.cursor.execute(
                "SELECT * FROM dinner"
            )
            data.append(self.cursor.fetchall())

            self.connection.commit()
            return data
        except Exception as e:
            print(e)
            return "Error: Database Select Error"
        finally:
            self.closeConnection()

    def selectMenuByDay(self, day):
        self.getConnection()
        data = []
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT course, menu FROM morning WHERE day=%s", day
            )
            data.append(self.cursor.fetchall())
            self.cursor.execute(
                "SELECT course, menu FROM lunch WHERE day=%s", day
            )
            data.append(self.cursor.fetchall())
            self.cursor.execute(
                "SELECT course, menu FROM dinner WHERE day=%s", day
            )
            data.append(self.cursor.fetchall())

            self.connection.commit()
            return data
        except Exception as e:
            print(e)
            return "Error: Database Select Error"
        finally:
            self.closeConnection()

    def selectMenuReview(self):
        self.getConnection()

        try:
            pass
        except:
            pass
        finally:
            self.closeConnection()
        pass

    def updateMenuReview(self):
        self.getConnection()

        try:
            pass
        except:
            pass
        finally:
            self.closeConnection()
        pass

    def insertMenuReview(self):
        self.getConnection()

        try:
            pass
        except:
            pass
        finally:
            self.closeConnection()
        pass