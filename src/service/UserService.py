from flask import request
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import session
import bcrypt
import re
import src.repository.UserRepository as UserRepository

class UserService:
    #회원가입
    def regist(self, id, pw):

        #아이디 기준
        if len(id) < 8 or len(id) > 12 and not re.findall("[a-zA-Z0-9]+",id):
            flash("아이디 기준에 맞지 않습니다.")     

        #비밀번호 기준
        if len(pw) < 8 or len(pw) > 15 and not re.findall("[a-zA-Z0-9]",pw) or not re.findall("[~!@#$%^&*()_,.]",pw):
            flash("비밀번호 기준에 맞지 않습니다.")

        pw = (bcrypt.hashpw(pw.encode('utf-8'),bcrypt.gensalt())).decode('utf-8')


        #아이디 존재여부 체크 false이면 유저 추가
        userRepository = UserRepository.UserRepository()
        #db_user = userRepository.db_connection()
        add_user = userRepository.useradd(id,pw)

        return add_user
        

    #로그인
    def login(self,id,pw):

        #로그인 시도 횟수 
        try:
            attempt = session['attempt']
            if attempt == 0:
                flash("로그인 시도 횟수를 초과하였습니다.")
                return render_template("/member/login.html")
            else:
                session['attempt'] -= 1
        
        except KeyError:
            attempt = session['attempt'] = 5

        # 데이터 유효성 체크
        if len(id) < 8 or len(id) > 12 and not re.findall("[a-zA-Z0-9]+",id):
            flash("아이디 기준에 맞지 않습니다.")
            #return render_template("/templates/member/login.html")
        if len(pw) < 8 or len(pw) > 15 and not re.findall("[a-zA-Z0-9]",pw) or not re.findall("[~!@#$%^&*()_,.]",pw):
            flash("비밀번호 기준에 맞지 않습니다.")
            #return render_template("/templates/member/login.html")
        
        userRepository = UserRepository.UserRepository() 

        #아이디 존재하는지
        check_id = self.check_userId(id) 
        #비밀번호가 맞는지
        check_idpw = self.check_userIdPw(id,pw)
        
       
        # 성공
        if check_id:
            if check_idpw:
                # 사용자 명으로 세션을 생성한다
                session['username'] = request.form['id']
                return redirect(url_for('home'))
    
    def check_userId(self, userid):
        userRepository = UserRepository.UserRepository() 
        answer = userRepository.findUserIdByUserId(userid)     

        if(len(answer) == 0): # 가져온 데이터가 없다면 false 있다면 true
            return False
        else:
            return True
        
    def check_userIdPw(self,input_username, input_password):
        userRepository = UserRepository.UserRepository()
        # DB 비밀번호 조회
        password = userRepository.findByUserId(input_username)

        # DB에 계정 정보가 없으면 password == None
        if password == None: 
            return False
        
        # 사용자가 입력한 비밀번호와  DB에 있는 비밀번호와 비교
        if input_password == password:
            return True
        else:
            return False


        
      


