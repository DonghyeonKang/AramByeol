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

    #TODO TESTING
    def selectMenuReview(self, menu_id):
        self.getConnection()
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT score FROM review WHERE menu_id=%s", menu_id
            )
            score = self.cursor.fetchall()
            return score
        except Exception as e:
            print(e)
            return "Error: Database Select Error"
        finally:
            self.closeConnection()

    #TODO TESTING
    def updateMenuReview(self, menu_id, score, lastScore):
        self.getConnection()

        try:
            self.cursor = self.connection.cursor()
            # score 를 가져온다. 
            self.cursor.execute(
                "SELECT score, review_count FROM review WHERE menu_id=%s", menu_id
            )
            # TODO 여기 fetchall 로 가져온 데이터 받는 거 수정 필요
            scoreInDb, review_count = self.cursor.fetchall()

            # lastScore를 뺀 다음 score 를 더한다.
            arr = []
            arr.append(scoreInDb - lastScore + score)
            arr.append(review_count)
            arr.append(menu_id)
            self.cursor.execute(
                "UPDATE review SET score=%s, review_count=%s WHERE menu_id=%s", arr
            )
            # TODO 리턴 값 어떻게 처리할 건지
            return "SUCCESS"
        except Exception as e:
            print(e)
            return "Error: Database UPDATE Error"
        finally:
            self.closeConnection()

    #TODO TESTING
    def insertMenuReview(self, menu_id, score):
        self.getConnection()

        try:
            # 리뷰 카운트를 가져온다. 
            self.cursor = self.connection.cursor()


            self.cursor.execute(
                "SELECT score, review_count FROM review WHERE menu_id=%s", menu_id
            )
            # TODO 여기 fetchall 로 가져온 데이터 받는 거 수정 필요
            scoreInDb, review_count =  self.cursor.fetchall()
            # 리뷰 카운트를 1올려 score와 함께 저장한다. 
            arr = []
            arr.append(score + scoreInDb)
            arr.append(review_count + 1)
            arr.append(menu_id)
            self.cursor.execute(
                "UPDATE review SET score=%s, review_count=%s WHERE menu_id=%s", arr
            )
            
            return "success"
        except Exception as e:
            print(e)
            return "Error: Database INSERT Error"
        finally:
            self.closeConnection()