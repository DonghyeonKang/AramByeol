import pymysql.cursors
import src.security.db_auth as db_auth

class AuthRepository:
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

    def insertRefreshToken(self, user_id, refreshToken):
        self.getConnection()
        try:
            cursor = self.connection.cursor()
            arr = [refreshToken, user_id]
            cursor.execute("INSERT INTO token(refresh_token, user_id) VALUES (%s, %s)", arr)
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "DB Insert Error"
        finally:
            self.closeConnection()

    def deleteRefreshToken(self, user_id):
        self.getConnection()
        try:
            cursor = self.connection.cursor()
            arr = [user_id]
            cursor.execute("DELETE FROM token WHERE user_id=%s", arr)
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "DB Insert Error"
        finally:
            self.closeConnection()

    def checkRefreshToken(self, refreshToken):
        self.getConnection()
        try:
            cursor = self.connection.cursor()
            arr = [refreshToken]
            cursor.execute("select refresh_token from token where refresh_token=%s", arr)
            rows = cursor.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)
        finally:
            self.closeConnection()
    
    def checkUserId(self, user_id):
        self.getConnection()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = %s", user_id)
            rows = cursor.fetchall()

            if(len(rows) == 0): # 가져온 데이터가 없다면 false 있다면 true
                return "Available"
            else:
                return "Already exists"
        except Exception as e:
            print(e)
            # TODO 여기 에러 처리 해야함
            return ""
        finally:
            self.closeConnection()

    def checkUserPw(self, user_id):
        self.getConnection()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = %s", user_id)
            row = cursor.fetchone()
            return row
        except Exception as e:
            print(e)
            # TODO 여기 에러 처리 해야함
            return ""
        finally:
            self.closeConnection()

    def updateUserPw(self, user_id, user_pw):
        self.getConnection()
        try:
            cursor = self.connection.cursor()
            arr = [user_pw, user_id]
            cursor.execute("UPDATE users SET user_pw=%s WHERE user_id=%s", arr)
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            # TODO 여기 에러 처리 해야함
            return "DB Update Error"
        finally:
            self.closeConnection()

    def insertUser(self, user_id, user_pw, nickname):
        self.getConnection()

        try:
            cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
            sql = "INSERT INTO users(user_id, user_pw, nickname) VALUES ('%s', '%s', '%s')" % (user_id, user_pw, nickname)  # 쿼리문 작성
            cursor.execute(sql) # 쿼리 실행 
            self.connection.commit() # 쿼리 적용
            return "success"
        except Exception as e:
            print(e)
            return ""
        finally:
            self.closeConnection()

    def checkNickname(self, nickname):
        self.getConnection()

        try:
            cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
            arr = [nickname]
            cursor.execute("SELECT user_id FROM users WHERE nickname=%s", arr) # 쿼리 실행 
            rows = cursor.fetchall()
            if len(rows) == 0:
                return "Available"
            else:
                return "Already exists"
        except Exception as e:
            print(e)
            return ""
        finally:
            self.closeConnection()

    def getNickname(self, user_id):
        self.getConnection()

        try:
            cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
            arr = [user_id]
            cursor.execute("SELECT nickname FROM users WHERE user_id=%s", arr) # 쿼리 실행 
            rows = cursor.fetchall()
            return rows[0]['nickname']
        except Exception as e:
            print(e)
            return ""
        finally:
            self.closeConnection()

    def updateNickname(self, userId, nickname):
        self.getConnection()

        try:
            cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
            arr = [nickname, userId]
            cursor.execute("UPDATE users SET nickname=%s WHERE user_id=%s", arr) # 쿼리 실행 
            self.connection.commit() # 쿼리 적용
            return "success"
        except Exception as e:
            print(e)
            return ""
        finally:
            self.closeConnection()

    def deleteUser(self, userId):
        self.getConnection()

        try:
            cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
            arr = [userId]
            cursor.execute("DELETE FROM users WHERE user_id=%s", arr) # 쿼리 실행 
            self.connection.commit() # 쿼리 적용
            cursor.execute("DELETE FROM token WHERE user_id=%s", arr) # 쿼리 실행 
            self.connection.commit() # 쿼리 적용
            return "success"
        except Exception as e:
            print(e)
            return ""
        finally:
            self.closeConnection()
    
    def getUid(self, userId):
        self.getConnection()

        try:
            cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
            arr = [userId]
            cursor.execute("SELECT id FROM users WHERE user_id=%s", arr) # 쿼리 실행 
            result = cursor.fetchall()
            return result[0]['id']
        except Exception as e:
            print(e)
            return ""
        finally:
            self.closeConnection()