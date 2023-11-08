import pymysql

class ViewRepository:
    def getConnection(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='aram',
                                     password='aramworrior',
                                     db='arambyeol',
                                     charset='utf8',
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
