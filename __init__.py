from flask import Flask # flask start 
from flask import request # html request 
from flask import render_template # rendering
from flask import session # session
from flask import redirect # move page
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import *
from user import *
import bcrypt

app = Flask(__name__)
app.secret_key = 'arambyeol'

# page route
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/member/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['password']
        pw = (bcrypt.hashpw(pw.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')  # 해싱 처리
        if(check_userId(id) != True):   # id 가 이미 존재하면 true
            useradd(id, pw)
        else:
            print("이미 존재하는 아이디")
        return redirect('http://localhost:5001/member/login.html')
    return render_template("/member/register.html")

@app.route('/member/login.html', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        id = request.form['id']
        pw = request.form['password']
        check_password = login_check(id, pw)
        print(check_password)
        if check_password:
            session['username'] = request.form['id']  # session id 부여
            return "%s님 환영합니다!" % id
        else:
            return "비밀번호 틀림"
    return render_template("/member/login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)   # 세션 내에 id 가 있으면 지움
    return render_template("index.html")

# review request
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
