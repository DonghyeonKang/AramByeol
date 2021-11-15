from flask import Flask # flask start 
from flask import request # html request 
from flask import render_template # rendering
from flask import session # session
from flask import redirect # move page
from flask import jsonify
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import *
from user import *
import bcrypt
import pymysql.cursors # python과 mysql(mariadb) 연동
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'arambyeol'

connection = pymysql.connect(host='localhost',
                        user='opc',
                        password='111111',
                        db='arambyeol',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)

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

# API
@app.route('/api/list', methods=['GET'])
def week():
    cursor = connection.cursor()

    sql = "select * from week"
    cursor.execute(sql)

    rows = cursor.fetchall()
    days = []
    for i in range(len(rows)):
        temp = []
        day = rows[i]['day'] # db에서 불러올 때 [배열][딕셔너리] 형식으로 들고옴.
        date = rows[i]['date']
        temp.append(day)
        temp.append(date)
        days.append(temp)

    day = []
    now = datetime.today().strftime("%Y-%m-%d")
    tomorrow = (datetime.today() + timedelta(1)).strftime("%Y-%m-%d")
    after = (datetime.today() + timedelta(2)).strftime("%Y-%m-%d")

    today_temp = ""
    tomorrow_temp = ""
    after_temp = ""
    for i in range(len(rows)):
        if (now == rows[i]['date']):
            today_temp = rows[i]['day']
        if (tomorrow == rows[i]['date']):
            tomorrow_temp = rows[i]['day']
        if (after == rows[i]['date']):
            after_temp = rows[i]['day']
    day.append(today_temp)
    day.append(tomorrow_temp)
    day.append(after_temp)

    sql = "select * from morning"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    morning = [] # 아침 정보를 제공해줄거얌
    for i in range(len(rows)):
        temp=[]
        for j in range(len(day)):
            if day[j] == rows[i]['day'] :
                temp.append(rows[i]['day'])
                temp.append(rows[i]['course'])
                temp.append(rows[i]['menu'])
                morning.append(temp)


    sql = "select * from lunch"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    lunch = []  # 점심 정보를 제공해 줄거얌
    for i in range(len(rows)):
        temp=[]
        for j in range(len(day)):
            if day[j] == rows[i]['day'] :
                temp.append(rows[i]['day'])
                temp.append(rows[i]['course'])
                temp.append(rows[i]['menu'])
                lunch.append(temp)
    

    sql = "select * from dinner"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    dinner = [] # 저녁 정보를 제공해 줄거얌
    for i in range(len(rows)):
        temp=[]
        for j in range(len(day)):
            if day[j] == rows[i]['day'] :
                temp.append(rows[i]['day'])
                temp.append(rows[i]['course'])
                temp.append(rows[i]['menu'])
                dinner.append(temp)
    # connection.commit()
    # connection.close()
    return jsonify({'days':days, 'morning':morning, 'lunch':lunch, 'dinner':dinner}) # js와 매칭



if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True, threaded=True)
