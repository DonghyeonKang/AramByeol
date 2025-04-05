import pymysql
import repository.db_auth as db_auth

class ViewRepository:
    def getConnection(self):
        self.login = db_auth.db_login
        self.connection = pymysql.connect(host=self.login['host'],
                                     user=self.login['user'],
                                     password=self.login['password'],
                                     db=self.login['db'],
                                     charset=self.login['charset'],
                                     cursorclass=pymysql.cursors.DictCursor)

    def closeConnection(self):
        self.connection.close()

    def selectView(self):
        self.getConnection()

        data = -1
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT views FROM views"
            )
            data = self.cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            self.closeConnection()

        return data
    
    def updateView(self):
        self.getConnection()

        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "UPDATE views SET views =views.views+1 where id = 1"
            )
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            self.closeConnection()
