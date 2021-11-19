from flask import Flask # flask start 
from flask import request # html request 
from flask import render_template # rendering
from flask import session # session
from flask import redirect # move page
from flask import jsonify
from flask import url_for
from flask import flash # alert
from user import *
import bcrypt
import pymysql.cursors # python과 mysql(mariadb) 연동
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'arambyeol'    # 세션을 사용하기 위해 비밀키가 서명된 쿠키 사용

def db_connection():
    connection = pymysql.connect(host='localhost',
                            user='root',
                            password='111111',
                            db='arambyeol',
                            charset='utf8',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

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
            flash("이미 존재하는 아이디입니다!")
    return render_template("/member/register.html")

@app.route('/member/login.html', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        id = request.form['id']
        pw = request.form['password']
        check_id = check_userId(id)
        check_password = login_check(id, pw)
        print(check_id)
        print(check_password)
        if check_id:
            if check_password:
                session['username'] = request.form['id']  # session id 부여
                return redirect(url_for('home'))
            else:
                flash("아이디 또는 비밀번호가 잘못 입력 되었습니다.")
                return render_template("/member/login.html")    # 비밀번호 틀림
        else:
            flash("아이디 또는 비밀번호가 잘못 입력 되었습니다.")
            return render_template("/member/login.html")    # id 없음
    return render_template("/member/login.html")    # 페이지

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()   # 세션 내에 id 가 있으면 지움
    return "1"
# API
@app.route('/api/list', methods=['GET'])
def week():
    connection = db_connection()
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
    connection.close()
    return jsonify({'days':days, 'morning':morning, 'lunch':lunch, 'dinner':dinner}) # js와 매칭

# 별점주기 API
@app.route('/api/score', methods=['POST'])
def save_score():
    connection = db_connection()
    cursor = connection.cursor()

    name = request.form['menu_name']
    score = request.form['menu_score']

    cursor.execute("SELECT reviewcount, score from menudata where menu=%s", name)
    data = cursor.fetchall()
    db_reviewcount = 0
    db_score = 0
    avg = 0
    if data[0]['reviewcount'] == None:
        db_reviewcount = 0
    else:
        db_reviewcount = data[0]['reviewcount']
    if data[0]['score'] == None:
        db_score = 0
    else: 
        db_score = data[0]['score']
    db_score = (db_score * db_reviewcount) + int(score)
    db_reviewcount = db_reviewcount + 1
    avg = int(round(db_score / db_reviewcount))
    cursor.execute("UPDATE menudata SET score=%s, reviewcount=%s WHERE menu=%s", (avg, db_reviewcount, name))
    connection.commit()
    connection.close()
    return jsonify({'msg': name + "메뉴에 " + str(score) + "점 주셨습니다."})

@app.route('/api/menu_score', methods=['POST'])
def get_score():
    menu_name = request.form['menu_name']
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT score from menudata where menu=%s", menu_name)
    score = cursor.fetchall()
    if score[0]['score'] == None:
        score = 0
    else:
        score = score[0]['score']
    connection.close()
    return jsonify({'score':score})

# 세션 확인 API
@app.route('/api/session_check', methods=['POST'])
def session_check():
    if session.get('username'):
        return '1'
    return '0'

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True, threaded=True)