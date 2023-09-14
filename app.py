from flask import Flask # Flask start 
from flask import render_template # Rendering
from flask import redirect # Move page
from flask import url_for # Return defined route link to client
from flask import request
from flask import session
from flask import Response

app = Flask(__name__)
app.secret_key = 'asd1inldap123jwaw'     # 세션을 암호화하기 위해 비밀키가 서명된 쿠키 사용


if not app.debug: # 디버그 모드가 아니면
    import logging  # 로깅을 하기위한 모듈
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler( # 2000바이트가 넘어가면 로테이팅 백업 진행. 최대 파일 10개
        '../log/arambyeol_error.log', maxBytes=2000, backupCount=10)
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
    return render_template("index.html")

# 회원관리 ----------------------------------------------------
import src.service.UserService as UserService

@app.route('/user', methods=['GET'])
def getRegistPage():
    return render_template("/member/register.html")

@app.route('/user', methods=['POST'])
def register():
    id = request.form['id'] # id input 값 받아오기
    pw = request.form['password'] # pw input 값 받아오기
    print("회원가입 실행됨!")
    userService = UserService.UserService()
    registerUser = userService.regist(id, pw)

    return render_template("/member/login.html")

@app.route('/login', methods=['GET'])
def getLoginPage():
    return render_template("/member/login.html")

@app.route('/login', methods=['POST'])
def login():
    id = request.json['id']
    pw = request.json['password']

        
    userService = UserService.UserService()
    loginUser = userService.login(id,pw)

    return redirect(url_for('home'))

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
    return resp

@app.route('/menu', methods=['GET'])
def getMenuApp():
    menuService = MenuService.MenuService()
    resp = Response(response=menuService.getMenuApp(), mimetype="application/json")    
    return resp

# 별점 ---------------------------------------------------------
@app.route('/menu/score', methods=['POST'])
def setMenuScore():
    menuService = MenuService.MenuService()

    # 클라이언트로부터 메뉴와 점수를 전달받음
    menu = request.form['menu_name']
    score = request.form['menu_score']
    result = menuService.setMenuScore(menu, score)
    return result    

# 실행 ---------------------------------------------------------
if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=False, threaded=True)