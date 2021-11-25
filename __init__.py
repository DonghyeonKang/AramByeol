from flask import Flask # Flask start 
from flask import request # Html request 
from flask import render_template # Rendering
from flask import session # Session
from flask import redirect # Move page
from flask import jsonify # Return json form to client
from flask import url_for # Return defined route link to client
from flask import flash
from user import * # Login and Register
import bcrypt   # Password hash encrypt and decrypt
import pymysql.cursors # python과 mysql(mariadb) 연동
from datetime import datetime, timedelta # Time generator
import db_auth # Database login info

app = Flask(__name__)
app.secret_key = 'asd1inldap123jwaw'        # 세션을 암호화하기 위해 비밀키가 서명된 쿠키 사용

if not app.debug: # 디버그 모드가 아니면
    import logging  # 로깅을 하기위한 모듈
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler( # 2000바이트가 넘어가면 로테이팅 백업 진행. 최대 파일 10개
        '../log/arambyeol_error.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.WARNING) # WARNING 수준의 레벨들을 로깅
    app.logger.addHandler(file_handler)

# Error handler 401, 403, 404, 500
@app.errorhandler(500)
def internal_error(error):
    return render_template('/error/error.html'), 500
@app.errorhandler(404)
def page_not_found(error):
    return render_template('/error/error.html'), 404
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('/error/error.html'), 403
@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('/error/error.html'), 401

def db_connection(): # Database Connection
    login = db_auth.db_login
    connection = pymysql.connect(host=login['host'],
                            user=login['user'],
                            password=login['password'],
                            db=login['db'],
                            charset=login['charset'],
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

# page route
@app.route('/')
def home():
    return render_template("index.html")

# 회원가입 API
@app.route('/member/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': # post 방식으로 받아옴
        id = request.form['id'] # id input 값 받아오기
        pw = request.form['password'] # pw input 값 받아오기
        pw = (bcrypt.hashpw(pw.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')  # 해싱 처리
        if(check_userId(id) != True):   # id 가 이미 존재하면 true
            useradd(id, pw) # id와 pw를 
            return redirect(url_for('login')) # 로그인 화면으로 redirect
        else:
            flash("이미 존재하는 아이디입니다!") # 알림
    return render_template("/member/register.html") # 회원가입 화면으로 redirect

# 로그인 API
@app.route('/member/login.html', methods=['GET', 'POST'])
def login():
    if request.method == "POST": # post 방식으로 받아옴
        id = request.form['id'] # id input 값 받아오기
        pw = request.form['password'] # pw input 값 받아오기
        check_id = check_userId(id) # 아이디가 있으면 true
        check_password = check_userPassword(id, pw) # 비밀번호가 틀리면 false
        if check_id:
            if check_password:
                session['username'] = request.form['id'] # session 에 userid 넣기
                session.permanent = True # 브라우저가 종료되어도 session이 사라지지 않도록 설정. 시간을 설정하지 않으면, default 값은 31일.
                return redirect(url_for('home')) # index.html로 redirect 한다. 
            else:
                flash("아이디 또는 비밀번호가 잘못 입력 되었습니다.") # 알림
                return render_template("/member/login.html") # 비밀번호 틀리면 다시 로그인 창으로 redirect
        else:
            flash("아이디 또는 비밀번호가 잘못 입력 되었습니다.") # 알림
            return render_template("/member/login.html") # 로그인 창으로 redirect
    return render_template("/member/login.html") # 로그인 페이지로 redirect

# 로그아웃 API
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) # 서버에 있는 'username'세션 제거
    return "1"

# 세션 확인 API
@app.route('/api/session_check', methods=['POST'])
def session_check():
    if session.get('username'):     # session에 'username' id 를 가진 session이 존재하면
        return '1'
    return '0'

# 메뉴 API
@app.route('/api/list', methods=['GET'])
def week(): # 한 주의 메뉴를 리턴.
    connection = db_connection()
    cursor = connection.cursor()

    sql = "select * from week" # week 테이블의 모든 데이터
    cursor.execute(sql)

    rows = cursor.fetchall()
    days = []
    # 한 주의 날짜를 리스트 딕셔너리 형식으로 DB에서 추출
    for i in range(len(rows)):
        temp = []
        day = rows[i]['day'] # db에서 불러올 때 [배열][딕셔너리] 형식으로 들고옴.
        date = rows[i]['date']
        temp.append(day)
        temp.append(date)
        days.append(temp)

    # 오늘, 내일, 모레 날짜를 계산
    day = []
    now = datetime.today().strftime("%Y-%m-%d")
    tomorrow = (datetime.today() + timedelta(1)).strftime("%Y-%m-%d")
    after = (datetime.today() + timedelta(2)).strftime("%Y-%m-%d")

    # 오늘, 내일, 모레에 해당하는 날짜만 추출
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
    
    # 오늘, 내일, 모레에 해당하는 메뉴들만 추출
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

    # 클라이언트로부터 메뉴와 점수를 전달받음
    name = request.form['menu_name']
    score = request.form['menu_score']

    # 가져온 메뉴를 DB의 메뉴와 비교하여 누적 점수를 가져옴
    cursor.execute("SELECT reviewcount, score from menudata where menu=%s", name)
    data = cursor.fetchall()
    db_reviewcount = 0
    db_score = 0
    avg = 0

    # 점수가 하나도 없었다면 None이므로 0이라고 해줌.
    if data[0]['reviewcount'] == None:
        db_reviewcount = 0
    else:
        db_reviewcount = data[0]['reviewcount']
    if data[0]['score'] == None:
        db_score = 0
    else: 
        db_score = data[0]['score']
    
    # 계산 방식 : 1. DB -> (누적점수 / 별점준 사용자 수) = 총점
    # 2. DB <- ((총점 + 부여 점수) / 별점준 사용자 수 + 1)
    db_score = (db_score * db_reviewcount) + int(score)
    db_reviewcount = db_reviewcount + 1
    avg = int(round(db_score / db_reviewcount))
    cursor.execute("UPDATE menudata SET score=%s, reviewcount=%s WHERE menu=%s", (avg, db_reviewcount, name))
    connection.commit()
    connection.close()
    return jsonify({'msg': name + " 메뉴에 " + str(score) + "점 주셨습니다."})

# 모달 창에 해당 메뉴의 누적 점수를 리턴
@app.route('/api/menu_score', methods=['POST'])
def get_score():
    menu_name = request.form['menu_name']
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT score from menudata where menu=%s', menu_name)
    score = cursor.fetchall()
    if score[0]['score'] == None:
        score = 0
    else:
        score = score[0]['score']
    connection.close()
    return jsonify({'score':score})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True, threaded=True)