import src.auth.auth_repository as auth_repository
import json

class AuthService:
    authRepository = auth_repository.AuthRepository()

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

    #--------- /auth
    def selectRefeshToken(self): # refresh token이 데이터베이스에 존재하는 지 확인
        pass

    def selectSession(self): # 세션이 데이터베이스에 존재하는 지 확인
        pass

    def updateRefeshToken(self): # refreah token의 만료기간을 갱신함
        pass

    def deleteRefreshToken(self): # refresh token을 삭제함
        pass

    def createAccessToken(self): # 로그인 시 토큰 생성
        pass

    def verifyAccessToken(self): # access token 이 유효한 지 검증
        pass

    def createSession(self): # 웹 로그인 시 session 생성
        pass
    #--------- /auth/member
    def insertMember(self): # 회원 가입
        pass

    def selectMember(self): # id 확인
        pass

    def webLogin(self): # 웹 로그인
        pass

    def appLogin(self): # 앱 로그인
        pass

    def deleteMember(self): # 회원 탈퇴
        pass 