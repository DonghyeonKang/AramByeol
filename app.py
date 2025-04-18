from flask import Flask # Flask start 
from flask import render_template # Rendering
from flask import redirect # Move page
from flask import url_for # Return defined route link to client
from flask import request
from flask import session
from flask import Response
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'asd1inldap123jwaw'     # 세션을 암호화하기 위해 비밀키가 서명된 쿠키 사용


if not app.debug: # 디버그 모드가 아니면
    import logging  # 로깅을 하기위한 모듈
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler( # 2000바이트가 넘어가면 로테이팅 백업 진행. 최대 파일 10개
        'log/arambyeol_error.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.WARNING) # WARNING 수준의 레벨들을 로깅
    app.logger.addHandler(file_handler)

# 에러 -----------------------------------------------------
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


# 페이지 라우팅 --------------------------------------
@app.route('/')
def home():
    viewService = ViewService.ViewService()
    viewService.updateView()
    return render_template("index.html")

@app.route('/login', methods=['GET'])
def getLoginPage():
    return render_template("/member/login.html")

# 회원관리 ----------------------------------------------------
import src.service.UserService as UserService

@app.route('/user', methods=['GET'])
def getRegistPage():
    return render_template("/member/register.html")

@app.route('/user', methods=['POST'])
def register():
    id = request.form['id'] # id input 값 받아오기
    pw = request.form['password'] # pw input 값 받아오기
    userService = UserService.UserService()
    registerUser = userService.regist(id, pw)

    return render_template("/member/login.html")

@app.route('/login', methods=['POST'])
def login():
    id = request.json['id']
    pw = request.json['password']

    userService = UserService.UserService()
    result = userService.login(id,pw)
    return result

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) # 서버에 있는 'username'세션 제거
    return "1"

# 세션 확인 API
@app.route('/session', methods=['POST'])
def session_check():
    if session.get('username'):     # session에 'username' id 를 가진 session이 존재하면
        return '1'
    return '0'

# 조회수 ---------------------------------------------------------
import src.service.ViewService as  ViewService

@app.route('/views', methods=['GET'])
def getView():
    viewService = ViewService.ViewService()
    response = viewService.getView()
    return response

# 메뉴 ---------------------------------------------------------
import src.service.MenuService as MenuService

@app.route('/menu/web', methods=['GET'])
def getMenuWeb():
    menuService = MenuService.MenuService()
    resp = Response(response=menuService.getMenuWeb(), mimetype="application/json")    

    sendLogstash_userAccess('WEB')
    return resp

@app.route('/menu', methods=['GET'])
def getMenuApp():
    menuService = MenuService.MenuService()
    resp = Response(response=menuService.getMenuApp(), mimetype="application/json")    
    return resp

# 별점 ---------------------------------------------------------
@app.route('/menu/score', methods=['GET'])
def getMenuScore():
    menuService = MenuService.MenuService()

    # 클라이언트로부터 메뉴와 점수를 전달받음
    menu = request.args.get('menu_name')
    result = menuService.getMenuScore(menu)
    return result


@app.route('/menu/score', methods=['POST'])
def setMenuScore():
    menuService = MenuService.MenuService()

    # 클라이언트로부터 메뉴와 점수를 전달받음
    menu = request.form['menu_name']
    score = request.form['menu_score']
    result = menuService.setMenuScore(menu, score)
    return result    

# 스케줄러 ---------------------------------------------------------
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

def run_script():
    # 실행할 스크립트나 명령어를 여기에 추가
    subprocess.run(['python3', '/home/ubuntu/arambyeol/src/service/CrawlingService.py'])

# 백그라운드 스케줄러 생성
scheduler = BackgroundScheduler()
scheduler.add_job(run_script, 'cron', day_of_week='mon-fri', hour=1)

def start_scheduler():
    print("스케줄링 시작")
    scheduler.start()

# 애플리케이션이 종료될 때 스케줄러도 종료
def shutdown_scheduler(exception=None):
    scheduler.shutdown()

# logstash 전송_사용자 접속 로그 
def sendLogstash_userAccess(platformType):
    url = 'http://was-alb-692266129.ap-northeast-2.elb.amazonaws.com:8080/loggingAccessTime'
    now = datetime.now()

    data = {
        'accessTime': str(now.date()) + 'T' + str(now.strftime('%H:%M:%S')),
        'platformType': platformType
    }

    # POST 요청 보내기
    response = requests.post(url, json=data)

    # 응답 확인
    if response.status_code == 200:
        print("요청이 성공적으로 보내졌습니다.")
    else:
        print("요청 실패. 응답 코드:", response.status_code)

# logstash 전송_에러로그
def sendLogstash_error(platformType):
    url = 'http://123.123.123.12:5000'

    data = {
        'platformType': platformType
    }

    # POST 요청 보내기
    response = requests.post(url, data=data)

    # 응답 확인
    if response.status_code == 200:
        print("요청이 성공적으로 보내졌습니다.")
    else:
        print("요청 실패. 응답 코드:", response.status_code)

# 실행 ---------------------------------------------------------
if __name__ == '__main__':
    start_scheduler()
    app.run('0.0.0.0',port=80,debug=False, threaded=True)