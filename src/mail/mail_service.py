from operator import truediv
import random
from flask import jsonify
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from src.security.securities import *
import src.mail.mail_repository as mail_repository
from flask_jwt_extended import *
from flask_jwt_extended import create_access_token
from flask_jwt_extended import decode_token
from flask_jwt_extended import JWTManager
from jwt import ExpiredSignatureError
from datetime import timedelta # Time generator

class MailService:
    mailRepository = mail_repository.MailRepository()

    def __init__(self) -> None:
        pass
    
    def verify_email(self, receiver):
        mailList = receiver.split('@')
        print(mailList)
        if mailList[1] == 'gnu.ac.kr':
            return True
        else:
            return False

    def send_email(self, receiver):
        try:
            if self.verify_email(receiver):
                # TODO 체크 해봐야 함
                # 이전에 보냈던 기록이 있으면 삭제함
                if self.mailRepository.selectToken(receiver) != "no token":
                    self.deleteNumber(receiver)
                randNum = self.createNumber()
                msg = MIMEText('아람별 인증번호: ' + str(randNum))                   # 메일 본문 첨부
                msg['Subject'] = Header('hello', 'utf-8') # 메일 제목 첨부
                msg['From'] = 'arammailmaster@naver.com'       # 송신 메일
                msg['To'] = receiver        # 수신 메일
                result = self.saveNumber(receiver, randNum)
                with smtplib.SMTP_SSL('smtp.naver.com') as smtp: # (*)
                    smtp.login(sender, senderPassword)           # (**)
                    smtp.send_message(msg)
                
                return jsonify({"result" : "success"})
            return jsonify({"result" : "학교 메일을 사용해주세요"})
        except Exception as e:
            print(e)
            return jsonify({"result" : "SMTP error"})
    
    def authenticate(self, mail, number):
        result = self.checkNumber(mail, number)
        if result == True:
            return jsonify({"result":"success"})
        else:
            return jsonify({"result": result})

    # 100000 ~ 999999 범위의 난수 생성
    def createNumber(self):
        num = random.randrange(100000, 1000000)
        return num

    def saveNumber(self, userId, number):
        token = create_access_token(identity = number, expires_delta = timedelta(minutes=10))
        print(token)
        result = self.mailRepository.insertNumber(userId, token)
        return result

    def checkNumber(self, userId, number):
        selectResult = self.mailRepository.selectToken(userId)
        if selectResult == "no token":
            return "no token"
        else:
            try:
                payload = decode_token(selectResult)
                if payload['sub'] == number:
                    return True
                else:
                    return "wrong number"
            except ExpiredSignatureError as e:
                print(e)
                self.deleteNumber(userId)
                # self.deleteNumber(userId)
                return "expired"

    def deleteNumber(self, user_id):
        result = self.mailRepository.deleteNumber(user_id)
        return result

