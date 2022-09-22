
from functools import wraps
from flask import Flask # Flask start 
from flask import request # Html request 
from flask import render_template # Rendering
from flask import session # Session
from flask import redirect # Move page
from flask import jsonify # Return json form to client
from flask import url_for # Return defined route link to client
from flask import flash
from flask import make_response
from user import * # Login and Register
import bcrypt   # Password hash encrypt and decrypt
import pymysql.cursors # python과 mysql(mariadb) 연동
from datetime import datetime, timedelta # Time generator
import src.security.db_auth as db_auth # Database login info
import jwt
from jwt import ExpiredSignatureError
from flask_jwt_extended import *
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import decode_token
from flask_jwt_extended import JWTManager

import src.auth.auth_service as auth_service
import src.menu.menu_service as menu_service

app = Flask(__name__)
app.secret_key = 'asd1inldap123jwaw'        # 세션을 암호화하기 위해 비밀키가 서명된 쿠키 사용
app.config.update(
			DEBUG = True,
			JWT_SECRET_KEY = "adswoern!@#rwlenf@#$13rweT#^DSfsrtwer"
		)
jwt = JWTManager(app)

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
#    return render_template("/error/index.html")
    return render_template("index.html")

#--------------------------------------- 회원가입, 로그인 ---------------------------------------#
import src.auth.auth_service as auth_service

# 회원가입 API
@app.route('/member/register.html', methods=['POST'])
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


# 웹 로그인
@app.route('/member/login.html', methods=['POST'])
def login():
    if request.method == "POST": # post 방식으로 받아옴
        id = request.form['id'] # id input 값 받아오기
        pw = request.form['password'] # pw input 값 받아오기
        check_id = check_userId(id) # 아이디가 있으면 true
        check_password = check_userPassword(id, pw) # 비밀번호가 틀리면 false
        if check_id:
            if check_password:
                session.permanent = True # 브라우저가 종료되어도 session이 사라지지 않도록 설정. 시간을 설정하지 않으면, default 값은 31일.
                session['username'] = request.form['id'] # session 에 userid 넣기
                return redirect(url_for('home')) # index.html로 redirect 한다. 
            else:
                flash("아이디 또는 비밀번호가 잘못 입력 되었습니다.") # 알림
                return render_template("/member/login.html") # 비밀번호 틀리면 다시 로그인 창으로 redirect
        else:
            flash("아이디 또는 비밀번호가 잘못 입력 되었습니다.") # 알림
            return render_template("/member/login.html") # 로그인 창으로 redirect
    return render_template("/member/login.html") # 로그인 페이지로 redirect

# 웹 로그아웃 API
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

# 토큰 유효성 검사
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs): # *args, **kwargs 정해지지 않은 인자
        token = None
        inputData = request.get_json(silent=True)

        if inputData == None: # json 데이터가 없다면
            if 'access_token' in request.form:
                token = request.form['access_token']
                authService = auth_service.AuthService()
                if authService.verifyToken(token) == False:
                    return jsonify({'result' : 'EXPIRED_TOKEN'}), 401
            else:
                return jsonify({'result' : 'Token is missing!'}), 401
        else:
            if 'access_token' in inputData: # 토큰이 존재하면,
                token = inputData['access_token']
                authService = auth_service.AuthService()
                if authService.verifyToken(token) == False:
                    return jsonify({'result' : 'EXPIRED_TOKEN'}), 401
            else:
                return jsonify({'result' : 'Token is missing!'}), 401
        return f(*args, **kwargs)
    return decorated

# 앱 회원가입
@app.route('/member', methods=['POST'])
def registerByApp():
    authService = auth_service.AuthService()
    # 클라이언트로부터 요청된 값
    input_data = request.get_json()
    user_id = input_data['user_id']
    user_pw = input_data['user_pw']
    nickname = input_data['nickname']
    result = authService.addUser(user_id, user_pw, nickname)
    return result

# 앱 회원가입
@app.route('/member/password', methods=['POST'])
@token_required
def changePassword():
    authService = auth_service.AuthService()
    # 클라이언트로부터 요청된 값
    input_data = request.get_json()
    user_id = input_data['user_id']
    user_pw = input_data['user_pw']
    result = authService.changePassword(user_id, user_pw)
    return result


# 앱 닉네임 중복 확인
@app.route('/member/nickname', methods=['GET'])
def checkNickname():
    authService = auth_service.AuthService()
    nickname = request.args.get('nickname')
    result = authService.checkNickname(nickname)
    return result

# 앱 닉네임 변경
@app.route('/member/nickname', methods=['PUT'])
@token_required
def updateNickname():
    authService = auth_service.AuthService()
    input_data = request.get_json()
    nickname = input_data['nickname']
    user_id = input_data['user_id']
    result = authService.updateNickname(user_id, nickname)
    return result

# 앱 회원 탈퇴
@app.route('/member', methods=['DELETE'])
@token_required
def deleteUser():
    authService = auth_service.AuthService()
    input_data = request.get_json()
    userId = input_data['user_id']
    accessToken = input_data['access_token']
    refreshToken = input_data['refresh_token']

    result = authService.deleteUser(userId, accessToken, refreshToken)
    return result

# 앱 로그인
@app.route('/login/app', methods=['POST'])
def loginByApp():
    authService = auth_service.AuthService()
    # 클라이언트로부터 요청된 값
    input_data = request.get_json()
    user_id = input_data['user_id']
    user_pw = input_data['user_pw']

    resData = authService.appLogin(user_id, user_pw)
    return resData

# 앱 로그아웃
@app.route('/logout/app', methods=['POST'])
@token_required
def logoutByApp():
    authService = auth_service.AuthService()
    # 클라이언트로부터 요청된 값
    input_data = request.get_json()
    user_id = input_data['user_id']

    result = authService.appLogout(user_id)
    return result

# 토큰 갱신
@app.route('/member/auth', methods=['PUT'])
def renewToken():
    authService = auth_service.AuthService()
    # 클라이언트로부터 요청된 값
    input_data = request.get_json()
    user_id = input_data['user_id']
    reqRefreshToken = input_data['refresh_token']

    result = authService.renewToken(user_id, reqRefreshToken)
    return result

from src.mail import mail_service
# 앱 이메일 중복 확인
@app.route('/member/id', methods=['GET'])
def checkUserId():
    authService = auth_service.AuthService()
    userId = request.args.get('user_id')
    result = authService.checkUserId(userId)
    return result

# 이메일 인증
@app.route('/member/mail', methods=['POST'])
def sendMail():
    input_data = request.get_json()
    receiver = input_data['mail']
    mailService = mail_service.MailService()
    
    if mailService.verify_email(receiver):
        result = mailService.send_email(receiver)
        return result
    else:
        return jsonify({"result" : "error"})

# 앱 메일 인증 번호 확인
@app.route('/member/mail/number', methods=['POST'])
def authenticateMailNumber():
    input_data = request.get_json()
    mail = input_data['mail']
    number =  input_data['number']
    mailService = mail_service.MailService()
    result = mailService.authenticate(mail, number)
    return result

#--------------------------------------- 메뉴, 리뷰 ---------------------------------------#
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

    # cursor.execute('SELECT score from menudata where menu=%s', )
    # score = cursor.fetchall()

    # 오늘, 내일, 모레에 해당하는 메뉴들만 추출
    morning = [] # 아침 정보를 제공해줄거얌
    for i in range(len(rows)):
        temp=[]
        for j in range(len(day)):
            if day[j] == rows[i]['day'] :
                temp.append(rows[i]['day'])
                temp.append(rows[i]['course'])
                temp.append(rows[i]['menu'])                
                cursor.execute('SELECT score from menudata where menu=%s', temp[2])
                test = cursor.fetchall()
                temp.append(test[0]['score'])
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
                cursor.execute('SELECT score from menudata where menu=%s', temp[2])
                test = cursor.fetchall()
                temp.append(test[0]['score'])
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
                cursor.execute('SELECT score from menudata where menu=%s', temp[2])
                test = cursor.fetchall()
                temp.append(test[0]['score'])
                dinner.append(temp)
    connection.close()
    print(morning)
    return jsonify({'days':days, 'morning':morning, 'lunch':lunch, 'dinner':dinner}) # js와 매칭

# 웹 메뉴 API
@app.route('/menu', methods=['GET'])
def get_menu():
    menuService = menu_service.MenuService()
    data = menuService.selectMenuList()
    return data

# 앱 메뉴 별점 가져오기
@app.route('/menu/review', methods=['GET'])
def select_review():
    menuService = menu_service.MenuService()
    inputList = request.get_json()
    menu_id = inputList['reviewData']
    result = menuService.selectMenuReview(menu_id)
    return result

# 앱 메뉴 별점 등록
@app.route('/menu/review', methods=['POST'])
@token_required
def update_review():
    menuService = menu_service.MenuService()
    inputList = request.get_json()
    reviewData = inputList['reviewData']
    resData = menuService.updateMenuReview(reviewData)
    return resData

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
    print(menu_name)
    cursor.execute('SELECT score from menudata where menu=%s', menu_name)
    score = cursor.fetchall()
    if score[0]['score'] == None:
        score = 0
    else:
        score = score[0]['score']
    connection.close()
    return jsonify({'score':score})

#--------------------------------------- 조회수 ---------------------------------------#
@app.route('/api/views', methods=['GET'])
def getViews():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT views from views')
    views = cursor.fetchall()
    connection.close()
    addViews(views)
    return jsonify({'views':views})

def addViews(views):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE views SET views=%s', views[0]['views'] + 1)
    connection.commit()
    connection.close()

@app.route('/api/setcookie', methods=['POST'])
def setCookie():
    if request.method == 'POST':
        user = request.form["nm"]
    
    resp = make_response()
    resp.set_cookie("userid", user)
    return resp

#--------------------------------------- 포스팅 ---------------------------------------#
#TODO posting 시 사진만 넘어오는 게 아니라 많은 정보가 넘어옴
#  posting 모듈을 만들어서 그곳에 데이터를 넘겨줘야할 듯 싱글톤 객체를 생성하는 방식으로 구현해보자
import src.posting.posting_service as posting_service
import base64
import PIL
from PIL import Image
from io import BytesIO

@app.route('/post/detail', methods=['GET']) # 출력
def getPost():
    postingService = posting_service.PostingService()
    postId = request.args.get('post_id')
    return postingService.selectPost(postId)

@app.route('/post/detail', methods=['POST']) # 삽입
@token_required
def insertPost():
    inputData = request.get_json()
    postingService = posting_service.PostingService()
    authService = auth_service.AuthService()
    user_id = inputData['user_id']
    # 객체 생성 이미지 저장 및 저장 path 생성   
    # TODO image 가 없으면 400 에러 난다. 이미지가 없어도 동작하도록
    try:
        strImage = inputData['image']
        img = Image.open(BytesIO(base64.b64decode(strImage)))
        path = postingService.saveImage(img, user_id)
        # 저장할 data 생성
        uid = authService.getUid(user_id)
        now = datetime.now()
        data = [uid, inputData['title'], inputData['content'], now.strftime('%Y-%m-%d %H:%M:%S'), int(inputData['score']), inputData['meal_time'], path]
        # 저장
        result = postingService.insertPost(data)
    except KeyError:
        uid = authService.getUid(user_id)
        now = datetime.now()
        data = [uid, inputData['title'], inputData['content'], now.strftime('%Y-%m-%d %H:%M:%S'), int(inputData['score']), inputData['meal_time']]
        result = postingService.insertPost(data)
    return jsonify({'result': result}) # success or fail

@app.route('/post/detail', methods=['PUT']) # 수정
def updatePost():
    inputData = request.get_json()    
    postId = inputData['post_id']
    postingService = posting_service.PostingService()
    user_id = inputData['user_id']
    # TODO image 가 없으면 400 에러 난다. 이미지가 없어도 동작하도록
    try:
        strImage = inputData['image']
        img = Image.open(BytesIO(base64.b64decode(strImage)))
        path = postingService.saveImage(img, user_id)
        # 저장할 data 생성
        now = datetime.now()
        data = [inputData['title'], inputData['content'], now.strftime('%Y-%m-%d %H:%M:%S'), int(inputData['score']), inputData['meal_time'], path]
        # 저장
        result = postingService.updatePost(postId, data)
    except KeyError:
        now = datetime.now()
        data = [inputData['title'], inputData['content'], now.strftime('%Y-%m-%d %H:%M:%S'), int(inputData['score']), inputData['meal_time']]
        result = postingService.updatePost(postId, data)
    return jsonify({'result': result}) # success or fail

@app.route('/post/detail', methods=['DELETE'])  # 삭제
def deletePost():
    inputData = request.get_json()
    postId = inputData['post_id']

    postingService = posting_service.PostingService()
    result = postingService.deletePost(postId)
    return result

@app.route('/post/list', methods=['POST']) # 포스팅 리스트를 가져옴
def getPostList():
    inputData = request.get_json()
    times = inputData['times']

    postingService = posting_service.PostingService()
    result = postingService.getPostList(times)
    return result

@app.route('/post/my', methods=['POST']) # 포스팅 리스트를 가져옴
@token_required
def getMyPost():
    inputData = request.get_json()
    user_id = inputData['user_id']

    postingService = posting_service.PostingService()
    result = postingService.getMyPost(user_id)
    return result

@app.route('/post/likes', methods=['POST']) # 포스팅 리스트를 가져옴
@token_required
def updateLikes():
    inputData = request.get_json()
    post_id = inputData['post_id']
    status = inputData['status']

    postingService = posting_service.PostingService()
    result = postingService.updateLikes(post_id, status)
    return result

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True, threaded=True)