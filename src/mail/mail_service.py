from flask_mail import Mail, Message
import random
from flask import jsonify

class MailService:
    def __init__(self, app) -> None:
        self.app = app
        self.app.config['MAIL_SERVER']='smtp.gmail.com'
        self.app.config['MAIL_PORT'] = 587
        self.app.config['MAIL_DEFAULT_SENDER'] = 'donghyeon009@gmail.com'
        self.app.config['MAIL_USE_TLS'] = True
        self.app.config['MAIL_USE_SSL'] = False
    
    def send_email(self, receiver):
        try:
            mail = Mail(self.app)
            randNum = self.createAuthenticationNumber()
            msg = Message('hello', recipients = [receiver])
            msg.body = '인증번호: %s' % randNum
            mail.send(msg)
            return jsonify({"result" : "success"})
        except Exception as e:
            print(e)
            return jsonify({"result" : "error"})
    
    # 100000 ~ 999999 범위의 난수 생성
    def createAuthenticationNumber(self):
        num = random.randrange(100000, 1000000)
        return num