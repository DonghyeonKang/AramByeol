from flask_mail import Mail, Message
import random
from flask import jsonify

class MailService:
    def __init__(self, app) -> None:
        self.app = app
        self.app.config['MAIL_SERVER']='smtp.gmail.com'
        self.app.config['MAIL_PORT'] = 25
        self.app.config['MAIL_DEFAULT_SENDER'] = 'mailmaster@arambyeol.kro.kr'
        self.app.config['MAIL_USE_TLS'] = False
        self.app.config['MAIL_USE_SSL'] = True
    
    def send_email(self, receiver):
        try:
            mail = Mail(self.app)
            randNum = self.createAuthenticationNumber()
            msg = Message('인증번호: %s' % randNum, recipients = receiver)
            print(receiver)
            print(receiver)
            print(receiver)
            mail.send(msg)
            return jsonify({"result" : "success"})
        except Exception as e:
            print(e)
    
    # 100000 ~ 999999 범위의 난수 생성
    def createAuthenticationNumber(self):
        num = random.randrange(100000, 1000000)
        return num