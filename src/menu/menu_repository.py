import pymysql.cursors
import src.security.db_auth as db_auth

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
                "SELECT menudata.menu_id, menu, score, course FROM menudata, morning WHERE menudata.menu_id = morning.menu_id AND day=%s", day
            )
            data.append(self.cursor.fetchall())
            self.cursor.execute(
                "SELECT menudata.menu_id, menu, score, course FROM menudata, lunch WHERE menudata.menu_id = lunch.menu_id AND day=%s", day
            )
            data.append(self.cursor.fetchall())
            self.cursor.execute(
                "SELECT menudata.menu_id, menu, score, course FROM menudata, dinner WHERE menudata.menu_id = dinner.menu_id AND day=%s", day
            )
            data.append(self.cursor.fetchall())

            self.connection.commit()
            return data
        except Exception as e:
            print(e)
            return "Error: Database Select Error"
        finally:
            self.closeConnection()

    #TODO TESTING
    def selectMenuReview(self, menu_id):
        self.getConnection()
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT score FROM review WHERE menu_id=%s", menu_id
            )
            score = self.cursor.fetchall()
            return score[0]
        except Exception as e:
            print(e)
            return "Error: Database Select Error"
        finally:
            self.closeConnection()

    #TODO TESTING
    def updateMenuReview(self, menu_id, score, user_id):
        self.getConnection()
        print(menu_id, score, user_id)
        try:
            # 리뷰 카운트를 가져온다. 
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT score, review_count FROM menudata WHERE menu_id=%s", menu_id
            )
            data =  self.cursor.fetchall()
            scoreInDb = data[0]['score']
            reviewCount = data[0]['review_count']

            # 메뉴 별 score 저장.
            arr = [round((score + scoreInDb * reviewCount) / (reviewCount + 1), 1), reviewCount + 1, menu_id]
            print(arr)
            self.cursor.execute(
                "UPDATE menudata SET score=%s, review_count=%s WHERE menu_id=%s", arr
            )
            self.connection.commit()

            # 사용자 별 score 저장.
            arr = [user_id, menu_id, float(score), float(score)]
            self.cursor.execute(
                "INSERT INTO `review` (user_id, menu_id, score) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE score=%s", arr
            )
            self.connection.commit()

            # 리뷰를 입력한 메뉴의 데이터를 반환한다. 
            self.cursor.execute(
                "SELECT menu_id, score FROM review WHERE menu_id=%s", menu_id
            )
            result = self.cursor.fetchall()
            return result[0]
        except Exception as e:
            print(e)
            return "Error: Database UPDATE Error"
        finally:
            self.closeConnection()